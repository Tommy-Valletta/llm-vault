# Scoped acquisition through existing tools

For history coverage metadata, wrap exports as `{records: [...], collection: {complete: false, gaps: [strings]}}` for normalized input, `{reviews: [...], comments: [...], collection: ...}` for GitHub, or `{discussions: [...], collection: ...}` for GitLab. Set complete false whenever selected pages or discussions are missing. Unknown completeness stays unknown; it never means the user's whole history was collected. Incomplete coverage enters the inferred profile's limitations.

Use this only when the user requests gathering examples or changes. Ask for missing repository/reviewer/date or PR/MR selection; do not crawl unrelated accounts. Gather only within that scope. Record collection limits, missing pages and permission failures privately. If collection is incomplete, do not present it as the complete reviewer history.

Prefer an existing session connector. Otherwise inspect available `gh`/`glab` access using read-only commands. Do not print credentials or inspect credential files. No tool/access means explain the limitation and accept exported JSON/JSONL. No new backend or model API is required.

GitHub examples: gather selected review summaries and inline comment threads, preserving parent IDs and optional diff hunks. Export `{reviews: [...], comments: [...]}` using the API-shaped records. GitLab examples: export selected merge-request discussion objects with their `notes`; system notes are excluded. Pagination must be exhausted within the declared selection or explicitly recorded incomplete. Include counter-discussion, not just favorable examples. Use the documented `--format github|gitlab` normalizer. Source authorization applies to processing, not public redistribution.

Remote changes normalize to `{repository, head_revision, files: [{path, patch, complete?}], gaps: [...]}`. Paths are repository-relative with forward slashes. Set `complete: false` when provider patches are truncated and record missing files in gaps. Supply a separate `{repository, revision, files: [{path, content}]}` source snapshot when context is needed. Fetch only selected files and ranges through the same existing session access; do not clone or execute an unreviewed repository to fetch context. Revision labels must match. The helper checks excerpt bytes against that snapshot but cannot independently authenticate the service response.

Live connector compatibility depends on session capability and permissions. This skill does not claim to ship GitHub/GitLab connectors. Do not POST comments or mutate reviews as part of acquisition.
