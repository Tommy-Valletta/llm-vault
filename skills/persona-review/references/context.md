# Context scope is separate from retrieval

`review prepare --context codebase|domain|none --retrieval auto|direct|indexed`.

- Codebase: gather relevant evidence within the chosen repository. Do not ingest everything by default.
- Domain: use repeated `--domain-path service/path` or a `--spec` with resolved symbol ranges. A selected controller is a code region, not general subject expertise. Do not use a domain to silently drop changed files from review.
- None: provide no surrounding source evidence. Useful as an ablation.
- Direct: use available read/search/symbol tools to select excerpts. Without explicit selections the helper captures one bounded window around the first added line of each changed file; this is limited context, not comprehensive dependency retrieval.
- Indexed: obtain scoped results through an existing index tool. Second Brain is one optional provider, not a requirement. No embeddings or index construction happen here.
- Auto: use an explicitly named provider when supplied; otherwise direct. An unavailable explicitly named index is an error, not silent direct fallback.

Direct selection JSON is an array of `{path, start_line, end_line}`. Pass it with `--context-selections`. A ContextSpec JSON (`--spec`) has `scope`, `retrieval`, `paths`, `symbols`, `provider`, `max_characters`; symbols are `{path, name, start_line, end_line}` resolved by existing tools. Select the actual definition/range, not all lexical matches to a name.

An index export (`--index-results`) has `{provider, repository, complete, evidence: [{path, start_line, end_line, excerpt, revision}]}`. Query only user-selected repositories/scopes. The helper filters outside-domain results and validates excerpts against accessible local source or a matching supplied snapshot. Stale mismatched excerpts are excluded. A changed revision with identical current excerpt is recorded as revalidated. Unverifiable results remain leads and are not supplied as authoritative evidence.

ContextBundle records the selected spec, actual retrieval, evidence with source locations/revisions/content hashes, omissions and outside-domain changed files. Read it before reviewing. If a dependency lies outside the domain, report the missing evidence and ask to expand scope only when needed. Do not expand automatically. Index availability does not prove freshness, isolation, or retrieval quality.
