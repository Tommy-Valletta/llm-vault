"""Portable CLI; AI reasoning is supplied by the invoking assistant."""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from uuid import uuid4
from dataclasses import asdict
from .artifacts import load, unseal, workspace, write, write_markdown
from .context import ContextSpec, capture_context, local_changes, normalize_changes
from .experiments import finalize_evaluation, prepare_evaluation
from .installation import install_skill
from .personas import finalize_distillation, import_history, prepare_distillation
from .workflow import finalize_review, markdown_report, prepare_review


def output_path(args, filename):
    return Path(args.out) if args.out else workspace()/uuid4().hex/filename


def parser():
    p=argparse.ArgumentParser(description='LLM Vault: assistant-guided personas and reviews. No model API calls.')
    commands=p.add_subparsers(dest='command',required=True)
    commands.add_parser('demo',help='Run the deterministic AST baseline, not an AI reviewer')
    commands.add_parser('doctor',help='Check prerequisites without changing configuration')
    h=commands.add_parser('history').add_subparsers(dest='action',required=True).add_parser('import')
    h.add_argument('--input',required=True);h.add_argument('--format',choices=['normalized','github','gitlab'],default='normalized')
    h.add_argument('--reviewer',action='append',default=[]);h.add_argument('--subject',choices=['reviewer','team'],default='reviewer')
    h.add_argument('--permitted',action='store_true',help='Confirm permission to process selected material with the assistant');h.add_argument('--out')
    d=commands.add_parser('distill').add_subparsers(dest='action',required=True)
    a=d.add_parser('prepare');a.add_argument('--history',required=True);a.add_argument('--style',choices=['none','general'],required=True);a.add_argument('--out')
    a=d.add_parser('finalize');a.add_argument('--request',required=True);a.add_argument('--draft',required=True);a.add_argument('--accept-draft',action='store_true');a.add_argument('--out')
    r=commands.add_parser('review').add_subparsers(dest='action',required=True)
    a=r.add_parser('prepare');source=a.add_mutually_exclusive_group(required=True);source.add_argument('--repo');source.add_argument('--changes')
    a.add_argument('--base',default='HEAD');a.add_argument('--profile',action='append',default=[]);a.add_argument('--generic',action='store_true')
    a.add_argument('--context',choices=['codebase','domain','none'],default='codebase');a.add_argument('--retrieval',choices=['auto','direct','indexed'],default='auto')
    a.add_argument('--domain-path',action='append',default=[]);a.add_argument('--spec',help='ContextSpec JSON, including resolved symbol ranges')
    a.add_argument('--provider');a.add_argument('--context-selections');a.add_argument('--index-results');a.add_argument('--source-snapshot');a.add_argument('--out')
    a=r.add_parser('finalize');a.add_argument('--request',required=True);a.add_argument('--response',required=True);a.add_argument('--out')
    e=commands.add_parser('evaluate',help='No subcommand: AST baseline; prepare/finalize: assistant ablations').add_subparsers(dest='action')
    a=e.add_parser('prepare');a.add_argument('--cases',required=True);a.add_argument('--profile',required=True);a.add_argument('--out')
    a=e.add_parser('finalize');a.add_argument('--control',required=True);a.add_argument('--responses',required=True);a.add_argument('--grades');a.add_argument('--out')
    a=commands.add_parser('skill').add_subparsers(dest='action',required=True).add_parser('install')
    a.add_argument('--dest',default=str(Path.home()/'.agents'/'skills'),help='Parent skill directory; use an explicit override for older host layouts')
    return p


def baseline(command):
    from .baseline import Change, LocalReviewer, compile_personas, review
    from .evaluation import evaluate
    root=Path(__file__).resolve().parent.parent
    personas=compile_personas(load(root/'fixtures'/'history.json'));cases=load(root/'fixtures'/'cases.json')
    if command=='evaluate':return evaluate(cases,personas)
    case=next(c for c in cases if c['id']=='synthetic-combined')
    return {'label':'Deterministic AST baseline, not persona distillation or AI review',**asdict(review(Change(**case['change']),personas,case['context'],LocalReviewer()))}


def execute(args):
    if args.command=='doctor':
        print(json.dumps({'python':sys.version.split()[0],'supported_python':sys.version_info>=(3,11),'git':bool(shutil.which('git')),
            'gh':bool(shutil.which('gh')),'glab':bool(shutil.which('glab')),'model_backend':'invoking assistant; no separate API key',
            'index_backend':'existing session tool only','notes':'Tool presence does not establish authentication. No configuration changed.'},indent=2));return 0
    if args.command=='demo' or (args.command=='evaluate' and args.action is None):
        print(json.dumps(baseline(args.command),indent=2));return 0
    if args.command=='skill':
        print('Installed self-contained skill at '+str(install_skill(args.dest)));return 0
    if args.command=='history':
        if not args.permitted:raise ValueError('Confirm eligibility and assistant processing with --permitted; this does not grant publication rights')
        source=Path(args.input)
        if source.suffix=='.jsonl':
            if source.stat().st_size>4_000_000:raise ValueError('Input exceeds byte budget')
            data=[json.loads(line) for line in source.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
        else:data=load(source)
        history,provenance=import_history(data,args.format,args.reviewer,args.subject)
        path=output_path(args,'history.json');prov=path.with_name(path.stem+'.provenance.json')
        if path.exists() or prov.exists():raise ValueError('Output already exists')
        write(path,history);write(prov,provenance)
    elif args.command=='distill':
        if args.action=='prepare':
            path=output_path(args,'distillation-request.json');write(path,prepare_distillation(load(args.history),args.style))
        else:
            path=output_path(args,'persona.json');write(path,finalize_distillation(load(args.request),load(args.draft),args.accept_draft))
    elif args.command=='review':
        if args.action=='prepare':
            changes=local_changes(args.repo,args.base) if args.repo else normalize_changes(load(args.changes))
            spec=ContextSpec(**load(args.spec)) if args.spec else ContextSpec(scope=args.context,retrieval=args.retrieval,paths=tuple(args.domain_path),provider=args.provider)
            context=capture_context(spec,changes,root=args.repo,selections=load(args.context_selections) if args.context_selections else (),
                indexed=load(args.index_results) if args.index_results else None,snapshot=load(args.source_snapshot) if args.source_snapshot else None)
            if args.repo and changes!=local_changes(args.repo,args.base):raise ValueError('Local change changed during capture; prepare again')
            path=output_path(args,'review-request.json');write(path,prepare_review(changes,context,[load(p) for p in args.profile],args.generic))
        else:
            report=finalize_review(load(args.request),load(args.response));path=output_path(args,'review.json');md=path.with_suffix('.md')
            if path.exists() or md.exists():raise ValueError('Output already exists')
            write(path,report);write_markdown(md,markdown_report(report))
            print('Review artifacts written to '+str(path));return 2 if report['payload']['status']=='partial' else 0
    elif args.command=='evaluate':
        if args.action=='prepare':
            control,packets=prepare_evaluation(load(args.cases),load(args.profile));path=output_path(args,'evaluation')
            if path.exists():raise ValueError('Evaluation output directory already exists')
            for identifier,packet in packets.items():write(path/'packets'/(identifier+'.json'),packet)
            write(path/'control.json',control)
        else:
            control=load(args.control);data=unseal(control,'evaluation_control');root=Path(args.control).parent
            if not all(re.fullmatch(r'R-[a-f0-9]{16}',t['id']) for t in data['tasks']):raise ValueError('Invalid evaluation task ID')
            requests={t['id']:load(root/'packets'/(t['id']+'.json')) for t in data['tasks']}
            responses={t['id']:load(Path(args.responses)/(t['id']+'.json')) for t in data['tasks'] if (Path(args.responses)/(t['id']+'.json')).is_file()}
            result=finalize_evaluation(control,requests,responses,load(args.grades) if args.grades else None)
            path=output_path(args,'evaluation-report.json');write(path,result)
    print('Artifact written to '+str(path)+'. Preparation requires assistant reasoning; no model was called.')
    return 0


def main(argv=None):
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8',errors='backslashreplace')
    try:return execute(parser().parse_args(argv))
    except (ValueError,OSError,KeyError,TypeError,AttributeError,subprocess.SubprocessError) as exc:
        print('Cannot complete operation: '+(str(exc) if isinstance(exc,ValueError) else type(exc).__name__+'. Check input and tool access.'),file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
