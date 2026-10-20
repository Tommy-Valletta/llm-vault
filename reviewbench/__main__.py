import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .engine import Change, LocalReviewer, compile_personas, review
from .evaluation import evaluate


def main():
    parser = argparse.ArgumentParser(description='Run an offline synthetic review reconstruction')
    parser.add_argument('command', choices=['demo', 'evaluate'])
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    history = json.loads((root / 'fixtures' / 'history.json').read_text(encoding='utf-8'))
    cases = json.loads((root / 'fixtures' / 'cases.json').read_text(encoding='utf-8'))
    personas = compile_personas(history)
    if args.command == 'evaluate':
        output = evaluate(cases, personas)
    else:
        case = next(c for c in cases if c['id'] == 'synthetic-combined')
        output = {'label': 'Synthetic offline demonstration; not historical production output',
                  **asdict(review(Change(**case['change']), personas, case['context'], LocalReviewer()))}
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
