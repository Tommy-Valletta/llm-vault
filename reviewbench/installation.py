"""Self-contained local skill installation using the canonical Python source."""
from pathlib import Path
import hashlib
import json
import shutil
import tempfile
from .artifacts import require


def install_skill(destination):
    package=Path(__file__).resolve().parent
    source=package.parent/'skills'/'persona-review'
    if not source.is_dir():source=package.parents[2]
    require((source/'SKILL.md').is_file(), 'Skill resources unavailable; run from the clone or installed skill')
    target=Path(destination).expanduser().resolve()/'persona-review'
    require(not target.exists(), 'Skill destination exists; choose another destination or remove the old installation yourself')
    require(not target.is_symlink(), 'Installation cannot replace a symlink')
    target.parent.mkdir(parents=True,exist_ok=True)
    temporary=Path(tempfile.mkdtemp(prefix='.persona-review-',dir=target.parent))
    try:
        for name in ('SKILL.md','agents','references','scripts'):
            path=source/name
            if not path.exists():continue
            if path.is_dir():shutil.copytree(path,temporary/name,ignore=shutil.ignore_patterns('__pycache__','_runtime'))
            else:shutil.copyfile(path,temporary/name)
        runtime=temporary/'scripts'/'_runtime';runtime.mkdir(exist_ok=True)
        shutil.copytree(package,runtime/'reviewbench',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        fixtures=package.parent/'fixtures'
        if fixtures.is_dir():shutil.copytree(fixtures,runtime/'fixtures')
        inventory={p.relative_to(temporary).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in temporary.rglob('*') if p.is_file()}
        (temporary/'INSTALLATION_MANIFEST.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8')
        temporary.rename(target)
    except BaseException:
        shutil.rmtree(temporary)
        raise
    return target
