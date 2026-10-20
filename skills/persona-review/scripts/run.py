"""Use the bundled runtime after installation, or the canonical source in a clone."""
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
runtime=HERE/'_runtime'
source=HERE.parents[2]
sys.path.insert(0,str(runtime if (runtime/'reviewbench').is_dir() else source))
sys.dont_write_bytecode=True
from reviewbench.__main__ import main

if __name__=='__main__':raise SystemExit(main())
