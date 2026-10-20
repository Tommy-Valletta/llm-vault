"""Native Windows/macOS acceptance using synthetic data; private output only."""
import argparse
import json
import os
import platform
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from reviewbench.artifacts import write


def main():
    parser=argparse.ArgumentParser(description='Run candidate-only native tests; does not call a model or source host')
    parser.add_argument('--out',required=True,help='Private JSON report outside Git')
    args=parser.parse_args()
    if sys.version_info<(3,11):raise SystemExit('Python 3.11 or newer is required')
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    result=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
    doctor=subprocess.run([sys.executable,'-m','reviewbench','doctor'],cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
    report={'platform':platform.system(),'python':platform.python_version(),'tests_passed':result.returncode==0,
            'doctor':json.loads(doctor.stdout) if doctor.returncode==0 else None,
            'test_log':result.stdout+result.stderr,'claim':'Native helper tests, synthetic replay workflow and installation; not independent AI-quality evidence.',
            'manual_skill_acceptance':{'fresh_session_invocation':'pending','actual_assistant_distillation_and_review':'pending'}}
    write(args.out,report)
    print(json.dumps({k:report[k] for k in ('platform','python','tests_passed','claim')},indent=2))
    return result.returncode


if __name__=='__main__':raise SystemExit(main())
