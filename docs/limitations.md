# Limitations

- The included reviewer is a narrow AST baseline. It is not an LLM and does not demonstrate AI review accuracy.
- It handles complete before and after Python files, not arbitrary patches, repository checkout, cross-file changes, deleted-line findings, or other languages.
- Direct calls to `eval` are flagged even when their input is trusted. Aliases, indirection, dataflow, imports, and execution paths are not analyzed.
- Mutable literals in function defaults are recognized; constructor calls and other shared-state patterns are not.
- The logging check recognizes only direct calls through the name `logging` and field names listed by the synthetic policy. It cannot establish confidentiality or detect all sensitive data flows.
- Findings must land on changed lines. An issue anchored elsewhere, or caused by a deletion, may be missed.
- Input budgets and syntax parsing are convenience bounds, not a hardened sandbox. Do not expose this local demo as a service for hostile inputs without further work.
- Malformed adapter findings are rejected, but a well-formed false allegation can pass. Backend exceptions stop the review. No retries, provider isolation, confidence calibration, or model-injection evaluation are implemented.
- The fixtures are small, synthetic, and designed alongside the implementation. They do not support production quality, speed, savings, or generalization claims.
- The repository's earlier public setup commit is retained. The engine and evaluation material were newly reconstructed; no confidential implementation history is imported. Motivation is owner-reported; no confidential artifacts, quotations, incidents, statistics, or private evaluation results are published.
