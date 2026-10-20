"""Exact fixture matching. This is a regression check, not an AI benchmark."""
from dataclasses import asdict
from .engine import Change, LocalReviewer, review


def evaluate(cases, personas):
    tp = fp = fn = 0
    details = []
    for case in cases:
        if case.get('synthetic') is not True:
            raise ValueError('Only explicitly synthetic fixtures are accepted')
        result = review(Change(**case['change']), personas, case['context'], LocalReviewer(), case.get('concerns'))
        actual = {(f.rule, f.line) for f in result.findings}
        expected = {(f['rule'], f['line']) for f in case['expected']}
        tp += len(actual & expected); fp += len(actual - expected); fn += len(expected - actual)
        details.append({'case': case['id'], 'passed': actual == expected, 'output': asdict(result)})
    return {'label': 'New synthetic regression results for a deterministic AST baseline',
            'matching': 'exact rule and after-file line per fixture', 'cases': len(cases),
            'passed': sum(c['passed'] for c in details), 'true_positives': tp,
            'false_positives': fp, 'false_negatives': fn,
            'precision': tp / (tp + fp) if tp + fp else None,
            'recall': tp / (tp + fn) if tp + fn else None, 'details': details}
