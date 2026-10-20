"""Offline, bounded artifact I/O. Digests detect drift, not trust or authorship."""
from __future__ import annotations
import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath

VERSION = 1
MAX_BYTES = 4_000_000


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value, label, limit=20_000):
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= limit, f'Invalid {label}')
    return value


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def seal(kind, payload):
    item = {'schema_version': VERSION, 'kind': kind, 'payload': payload}
    return {**item, 'digest': digest(item)}


def unseal(item, kind):
    require(isinstance(item, dict) and item.get('kind') == kind and item.get('schema_version') == VERSION, 'Artifact kind/version mismatch')
    require(item.get('digest') == digest({k: item[k] for k in ('schema_version', 'kind', 'payload')}), 'Artifact changed since preparation')
    return item['payload']


def load(path):
    path = Path(path)
    require(path.stat().st_size <= MAX_BYTES, 'Input exceeds byte budget; narrow the selection')
    return json.loads(path.read_text(encoding='utf-8-sig'))


def private_output(path):
    path = Path(path).expanduser().absolute()
    require(not path.is_symlink(), 'Output cannot replace a symlink')
    # Resolve benign OS aliases (including macOS temporary directories) before
    # enforcing the actual destination's Git boundary. Exclusive writes remain.
    path=path.resolve()
    for parent in (path,*path.parents):
        require(not (parent / '.git').exists(), 'Private artifacts must be outside Git working trees')
    return path


def workspace():
    return Path(os.environ.get('LLM_VAULT_WORKSPACE', str(Path.home() / '.llm-vault' / 'workspaces')))


def write(path, value):
    path = private_output(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    return path


def write_markdown(path, value):
    path = private_output(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(value)


def relative_path(value):
    text(value, 'repository-relative path', 1000)
    require('\\' not in value and ':' not in value and '\x00' not in value, 'Invalid repository-relative path')
    path = PurePosixPath(value)
    require(not path.is_absolute() and all(p not in ('', '.', '..') for p in value.split('/')), 'Unsafe repository-relative path')
    require(all(p.casefold() != '.git' and p.rstrip(' .') == p and not re.match(r'^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)',p,re.I) for p in value.split('/')), 'Unsafe administrative or platform-specific source path')
    return value


def source_file(root, name):
    root = Path(root).resolve()
    name = relative_path(name)
    target = root / name
    for parent in (target, *target.parents):
        if parent == root:
            break
        require(not parent.is_symlink(), 'Source cannot traverse a symlink')
    require(target.resolve().is_relative_to(root), 'Source escapes selected repository')
    require(target.is_file(), 'Source file is unavailable')
    require(target.stat().st_size <= MAX_BYTES, 'Source file exceeds byte budget')
    return target
