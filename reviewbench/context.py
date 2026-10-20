"""Capture scoped evidence with existing tools. No indexer or network client."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
from pathlib import Path
import hashlib
import re
import subprocess
import shutil
from .artifacts import relative_path, require, seal, source_file, text, unseal


def git_read(root, *args):
    executable=shutil.which('git')
    require(executable is not None and not Path(executable).resolve().is_relative_to(Path(root).resolve()), 'A trusted Git executable outside the reviewed repository is required')
    result = subprocess.run([str(Path(executable).resolve()), '-c', 'core.fsmonitor=false', '-c', 'core.hooksPath=', *args], cwd=root, capture_output=True, timeout=30, check=True)
    return result.stdout


@dataclass(frozen=True)
class ContextSpec:
    scope: str = 'codebase'
    retrieval: str = 'auto'
    paths: tuple[str, ...] = ()
    symbols: tuple[dict, ...] = ()
    provider: str | None = None
    max_characters: int = 50_000

    def validate(self):
        require(self.scope in ('none', 'codebase', 'domain'), 'Unknown context scope')
        require(self.retrieval in ('auto', 'direct', 'indexed'), 'Unknown retrieval method')
        require(type(self.max_characters) is int and 0 < self.max_characters <= 180_000, 'Invalid context budget')
        for path in self.paths: relative_path(path)
        for symbol in self.symbols:
            relative_path(symbol['path']); text(symbol.get('name'), 'symbol', 200)
            require(type(symbol.get('start_line')) is int and type(symbol.get('end_line')) is int and 0 < symbol['start_line'] <= symbol['end_line'], 'Invalid selected symbol range')
        require(self.scope != 'domain' or bool(self.paths or self.symbols), 'Domain context needs paths or resolved symbol ranges')

    def allows(self, path, start=1, end=1):
        if self.scope == 'none': return False
        if self.scope == 'codebase': return True
        return any(path == p or path.startswith(p.rstrip('/') + '/') for p in self.paths) or any(path == s['path'] and start >= s['start_line'] and end <= s['end_line'] for s in self.symbols)


@dataclass
class ContextBundle:
    spec: dict
    repository: str
    actual_retrieval: str
    evidence: list[dict] = field(default_factory=list)
    gaps: list[dict] = field(default_factory=list)
    outside_scope_changes: list[str] = field(default_factory=list)


def capture_context(spec, changes, root=None, selections=(), indexed=None, snapshot=None):
    spec.validate()
    selected = unseal(changes, 'changes')
    method = 'indexed' if spec.retrieval == 'indexed' or (spec.retrieval == 'auto' and spec.provider) else 'direct'
    bundle = ContextBundle(asdict(spec), selected['repository'], 'none' if spec.scope == 'none' else method)
    if spec.scope == 'none': return seal('context', asdict(bundle))
    require(method != 'indexed' or (spec.provider and indexed is not None), 'Requested index is unavailable; supply scoped results from an existing tool or explicitly choose direct retrieval')
    if snapshot:
        require(snapshot.get('repository') == selected['repository'] and snapshot.get('revision') == selected['head_revision'], 'Source snapshot repository/revision does not match the change')
    snapshot_files = {relative_path(f['path']): f['content'] for f in (snapshot or {}).get('files', [])}
    require(sum(len(v) for v in snapshot_files.values()) <= 500_000, 'Source snapshot exceeds text budget')
    for change in selected['files']:
        if not spec.allows(change['path']) and not any(s['path'] == change['path'] for s in spec.symbols):
            bundle.outside_scope_changes.append(change['path'])
    if method == 'indexed':
        require(indexed.get('repository') == selected['repository'], 'Index results belong to a different repository')
        require(indexed.get('provider') == spec.provider, 'Index provider mismatch')
        candidates = indexed.get('evidence', [])
        if indexed.get('complete') is not True:
            bundle.gaps.append({'reason': 'index collection is incomplete'})
    else:
        candidates = list(selections)
        if not candidates:
            if spec.scope == 'domain' and spec.symbols:
                candidates += [{'path':s['path'],'start_line':s['start_line'],'end_line':s['end_line']} for s in spec.symbols]
            for change in selected['files']:
                if change.get('changed_lines'):
                    line = min(change['changed_lines'])
                    if any(n > line+35 for n in change['changed_lines']):
                        bundle.gaps.append({'path':change['path'],'reason':'additional changed regions are outside the default context window; select more evidence'})
                    if spec.scope=='domain' and spec.symbols and not any(change['path']==p or change['path'].startswith(p+'/') for p in spec.paths):
                        continue
                    candidates.append({'path': change['path'], 'start_line': max(1, line-15), 'end_line': line+35})
    require(len(candidates) <= 200, 'Too many context selections; narrow the selection')
    budget = 0
    for candidate in candidates:
        path = relative_path(candidate['path'])
        start, end = candidate.get('start_line', 1), candidate.get('end_line', 80)
        require(type(start) is int and type(end) is int and 0 < start <= end, 'Invalid context line range')
        if not spec.allows(path, start, end):
            bundle.gaps.append({'path': path, 'reason': 'outside selected context domain; scope was not expanded'}); continue
        try:
            if root is not None:
                content = source_file(root, path).read_text(encoding='utf-8')
                verification = 'local-source-read'
            else:
                require(path in snapshot_files, 'No accessible source snapshot')
                content = snapshot_files[path]; verification = 'provided-source-snapshot'
            require('\x00' not in content, 'Binary source')
        except (ValueError, OSError, UnicodeError):
            bundle.gaps.append({'path': path, 'reason': 'source unavailable or uninspectable; retrieval result remains an unverified lead'}); continue
        lines = content.splitlines()
        if start > len(lines):
            bundle.gaps.append({'path': path, 'reason': 'source range unavailable'}); continue
        end = min(end, len(lines)); excerpt = '\n'.join(lines[start-1:end])
        if method == 'indexed' and candidate.get('excerpt') != excerpt:
            bundle.gaps.append({'path': path, 'reason': 'stale or mismatched index excerpt; excluded'}); continue
        if method == 'indexed' and candidate.get('revision') != selected['head_revision']:
            bundle.gaps.append({'path': path, 'reason': 'index revision differs; excerpt revalidated against supplied source'})
        if budget + len(excerpt) > spec.max_characters:
            bundle.gaps.append({'path': path, 'reason': 'context budget exhausted; selection omitted'}); continue
        budget += len(excerpt)
        bundle.evidence.append({'id': 'C-' + hashlib.sha256((path+':'+str(start)+':'+str(end)+':'+excerpt).encode()).hexdigest()[:16],
            'path': path, 'start_line': start, 'end_line': end, 'excerpt': excerpt,
            'revision': selected['head_revision'], 'content_sha256': hashlib.sha256(content.encode()).hexdigest(), 'verification': verification})
    return seal('context', asdict(bundle))


def added_lines(patch):
    current = None; found = []
    for line in patch.splitlines():
        match = re.match(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@', line)
        if match: current = int(match.group(1)); continue
        if current is None: continue
        if line.startswith('+'):
            found.append(current); current += 1
        elif line.startswith(' '): current += 1
        elif line.startswith('-') or line.startswith('\\ No newline'): pass
        else: current = None
    return found


def normalize_changes(data):
    text(data.get('repository'), 'repository label', 300)
    text(data.get('head_revision'), 'head revision', 300)
    require(isinstance(data.get('files'), list) and 0 < len(data['files']) <= 200, 'Select 1–200 changed files')
    seen = set(); files = []; gaps = list(data.get('gaps', []))
    budget = 0
    for item in data['files']:
        path = relative_path(item['path']); require(path not in seen, 'Duplicate changed path'); seen.add(path)
        patch = item.get('patch', '')
        require(isinstance(patch, str), 'Change patch must be text')
        if item.get('binary') or '\x00' in patch or 'Binary files ' in patch:
            gaps.append({'path': path, 'reason': 'binary change excluded'}); continue
        if item.get('complete') is False:
            gaps.append({'path': path, 'reason': 'provider change patch is incomplete'})
        budget += len(patch); require(budget <= 250_000, 'Change exceeds text budget; select fewer files')
        files.append({'path': path, 'patch': patch, 'changed_lines': added_lines(patch)})
    require(bool(files), 'No inspectable text changes')
    return seal('changes', {'repository': data['repository'], 'head_revision': data['head_revision'], 'files': files, 'gaps': gaps})


def local_changes(root, base='HEAD'):
    root = Path(root).resolve()
    # Resolve revisions as data first; disable external diff/text conversion below.
    require(not base.startswith('-'), 'Invalid base revision')
    revision = git_read(root, 'rev-parse', '--verify', '--end-of-options', base+'^{commit}').decode().strip()
    paths = git_read(root, 'diff', '--no-ext-diff', '--no-textconv', '--no-renames', '--name-only', '-z', revision, '--').decode('utf-8').rstrip('\0').split('\0')
    require(any(paths), 'No tracked changes compared with the selected base')
    files = []
    for path in paths:
        relative_path(path)
        patch = git_read(root, 'diff', '--no-ext-diff', '--no-textconv', '--no-renames', '--unified=3', revision, '--', path).decode('utf-8')
        files.append({'path': path, 'patch': patch})
    untracked = git_read(root, 'ls-files', '--others', '--exclude-standard', '-z').decode('utf-8').strip('\0')
    gaps = [{'reason': 'untracked files are not included; stage intended additions or supply an exported change set'}] if untracked else []
    return normalize_changes({'repository': root.name, 'head_revision': 'worktree-at-'+revision, 'files': files, 'gaps': gaps})
