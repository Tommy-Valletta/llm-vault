# Reproduce the evaluation

From the repository root, run:

```text
python -m unittest discover -s tests -v
python -m reviewbench evaluate
```

The test runner checks both the synthetic fixture suite and orchestration behavior with test adapters. The evaluation command prints JSON with per-case output and aggregate counts. It reads only the two fixture files bundled here, parses source, and does not execute the proposed changes.

A true positive is an exact `(rule, after-file line)` match within a case. Unexpected pairs count as false positives and missing expected pairs as false negatives. Precision and recall are printed only for this fixture definition. Undefined ratios are `null`. Findings are scoped to added or replaced lines before scoring.

The cases cover individual rules, a combined change, corrected code, an unrestricted log field, absent context, an existing issue on an unchanged line, removal of an issue, a string containing a risky-looking expression, explicit reviewer selection, and a multiline function default.

The expected labels and source were authored together with the rules. There is no held-out corpus, independent human adjudication, external model comparison, latency study, or historical production comparison. Treat the result as a reproducible regression check.

To extend this evaluation, add independently labeled eligible fixtures, report false positives as well as missing findings, document the matching policy, and keep new evaluation results separate from claims about earlier work. Do not import private review histories.
