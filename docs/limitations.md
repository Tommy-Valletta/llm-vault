# Limitations

- The CLI does not perform AI inference. Distillation and actual review require the invoking assistant and its processing permissions. There is no unattended model backend.
- Existing session tools determine remote source and index access. The project does not ship connectors, account setup, embeddings or an indexer. Live compatibility is not established by mock response tests.
- Profiles can overgeneralize sparse examples or misinterpret disagreement. Evidence-ID validation and exact-phrase checks cannot prove faithful inference, privacy, permission, or resistance to semantic leakage. Inspect accepted drafts.
- Source and context can contain hostile instructions. Request separation and read-only helpers reduce accidental execution; they are not a model-injection guarantee or hardened service sandbox.
- Domain scopes use explicit paths or ranges resolved by existing navigation tools. There is no language-aware symbol resolver in the helper. Default direct windows are limited; dependencies require explicit selections.
- Index results require accessible source or matching supplied snapshots. Snapshot hashes detect drift but do not independently authenticate origin. Index isolation and search quality remain properties to validate in the provider.
- Findings are limited to added/replaced after-file lines. Deletion-only defects, binary changes and certain patch formats are not supported. Truncated provider patches and untracked local files are reported as gaps. No repository checkout, reviewed-code execution or target tests happen automatically.
- Valid findings can be incorrect. Exact duplicate handling is not semantic consensus; failures or missing context do not become a clean review.
- Current AI worked examples share their authoring session and are not independent benchmarks. Fixture/replay tests do not demonstrate general AI quality or original production effectiveness.
- The compatibility target is native Windows and macOS with Python 3.11+. Actual native checks and pending manual/fresh-session work must be read in validation.md; portable source alone is not proof of native operation.
- No historical operational measurements, distinctive incidents, private examples or confidential implementation history are published. Owner-reported authorship is separate from the newly authored public reconstruction.
