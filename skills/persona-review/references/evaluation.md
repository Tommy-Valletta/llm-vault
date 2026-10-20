# Assistant-guided paired experiments

`evaluate prepare --cases CASES.json --profile PROFILE.json --out PRIVATE_RUN_DIRECTORY` writes `control.json` and `packets/`. Case input is an array of `{id, changes, context, judgments: [{id, description}]}`; changes/context are captured sealed artifacts. The control contains scoring judgments and is not reviewer input. Packets contain only the change, permitted context, persona and review instructions.

Generic and persona conditions share exactly the same captured change and context digests. No-context removes surrounding evidence. No-style is added when a profile contains style. Retrieval comparisons should use separately captured context bundles; do not credit a persona for receiving better source evidence.

For meaningful assistant evaluation, open a fresh review session for each packet and provide only that packet plus the review response schema. Do not give the control, expected findings, other conditions' outputs or authoring discussion. If the host cannot isolate sessions, record `shared-session` and do not call the result independent or held-out. Do not create extra tasks or send source to other models/services without authorization.

Store responses under `RESPONSES/TASK_ID.json`. `evaluate finalize --control RUN/control.json --responses RESPONSES --out REPORT.json` validates them and reports missing/partial work. With no grading input, it makes no accuracy claim. Stored outputs must be labeled `run.kind: replay`.

Optional `--grades` accepts `{adjudicator: human|assistant, independent: boolean, decisions: [{task_id, finding_id, expected_id: string|null, rationale}]}`. Each returned finding must be adjudicated exactly once. Match a known expected issue ID or use null for a false positive; unmatched expected issues count as missed. Do not score incomplete or partial runs. State the matching rationale and who judged it. Schema validation cannot establish the truth of judgments or independence.

Record exact input/profile/request hashes and host/model metadata. A model field not exposed by the host is `unknown`; do not guess a model or fabricate cost/latency. The included AST baseline tests are regression checks, not persona-learning results or original operational measurements.
