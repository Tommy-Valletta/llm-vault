"""Paired-context ablations with separate reviewer packets and scoring material."""
from copy import deepcopy
from .artifacts import digest, require, seal, unseal
from .personas import validate_profile
from .workflow import finalize_review, prepare_review


def prepare_evaluation(cases, profile):
    persona = validate_profile(profile)
    require(0<len(cases)<=50, 'Select 1–50 evaluation cases')
    packets = {}; tasks = []; labels = {}; seen = set()
    for case in cases:
        case_id = case['id']; require(isinstance(case_id,str) and case_id and case_id not in seen, 'Invalid or duplicate evaluation case'); seen.add(case_id)
        labels[case_id] = case.get('judgments', [])
        require(isinstance(labels[case_id],list) and len({j['id'] for j in labels[case_id]})==len(labels[case_id]), 'Invalid judgment IDs')
        changes, context = case['changes'], case['context']
        conditions = {'generic':prepare_review(changes,context,generic=True), 'persona':prepare_review(changes,context,[profile])}
        empty = deepcopy(unseal(context,'context'));empty.update(evidence=[],gaps=[],outside_scope_changes=[],actual_retrieval='none')
        empty['spec']['scope']='none'
        conditions['no-context'] = prepare_review(changes,seal('context',empty),[profile])
        if persona.get('style'):
            without_style=deepcopy(persona);without_style['style']=None
            conditions['no-style']=prepare_review(changes,context,[seal('persona_profile',without_style)])
        for condition, request in conditions.items():
            task_id='R-'+digest([case_id,condition])[:16]
            packets[task_id]=request
            tasks.append({'id':task_id,'case_id':case_id,'condition':condition,'request_digest':request['digest'],
                          'changes_digest':request['payload']['changes_digest'],'context_digest':request['payload']['context_digest']})
    return seal('evaluation_control',{'tasks':tasks,'judgments':labels,'note':'Keep this scoring control away from reviewer sessions; reviewer packets contain no judgments.'}),packets


def finalize_evaluation(control, requests, responses, grades=None):
    data=unseal(control,'evaluation_control');reports={};missing=[]
    for task in data['tasks']:
        identifier=task['id']
        require(requests[identifier]['digest']==task['request_digest'],'Evaluation packet drift')
        if identifier not in responses:missing.append(identifier);continue
        reports[identifier]=finalize_review(requests[identifier],responses[identifier])
    result={'tasks':data['tasks'],'missing':missing,'reports':reports,'scoring':None,
            'limits':'Assistant runs are nondeterministic. Replays only test plumbing. Shared sessions are not independent experiments.'}
    if grades is not None:
        require(grades.get('adjudicator') in ('human','assistant'),'Label the adjudicator')
        require(type(grades.get('independent')) is bool,'State whether adjudication was independent')
        require(not missing and all(r['payload']['status']=='complete' for r in reports.values()),'Cannot score incomplete or partial runs')
        require(all(g.get('task_id') in reports for g in grades.get('decisions',[])), 'Grade belongs to an unknown evaluation task')
        scores={}
        for task in data['tasks']:
            task_id=task['id'];findings={f['id'] for f in reports[task_id]['payload']['findings']}
            expected={j['id'] for j in data['judgments'][task['case_id']]}
            entries=[g for g in grades.get('decisions',[]) if g.get('task_id')==task_id]
            accounted=set();matched=set()
            for decision in entries:
                finding=decision.get('finding_id');target=decision.get('expected_id')
                require(finding in findings and finding not in accounted,'Unknown or duplicate graded finding')
                require(isinstance(decision.get('rationale'),str) and bool(decision['rationale'].strip()),'Every grading decision needs rationale')
                accounted.add(finding)
                if target is not None:
                    require(target in expected and target not in matched,'Unknown or duplicate expected issue');matched.add(target)
            require(accounted==findings,'Adjudicate every returned finding, including false positives')
            scores[task_id]={'matched':len(matched),'false_positives':len(findings)-len(matched),'missed':len(expected)-len(matched)}
        result['scoring']={'adjudicator':grades['adjudicator'],'independent':grades['independent'],'per_task':scores,
            'evidence_label':'replay' if any(r['payload']['run']['kind']=='replay' for r in reports.values()) else 'assistant-run'}
    return seal('evaluation_report',result)
