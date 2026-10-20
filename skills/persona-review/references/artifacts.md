# Artifacts and reasoning handoff

Reviewer responses can include `limitations: [strings]` alongside findings. Use it to record uncertainty when captured evidence cannot establish an actionable issue. Those notes survive finalization; do not replace uncertainty with an invented finding.

Run `scripts/run.py --help` and each command's `--help` for arguments. Requests and finalized artifacts have `schema_version: 1`, `kind`, `payload` and a SHA-256 `digest`. Do not hand-edit sealed artifacts; regenerate them with the appropriate prepare step. Drafts and assistant responses are ordinary JSON.

Local normalized history is JSONL or a JSON array of `{id, text, author?, thread_id?, reply_to?, code_context?}`. `--reviewer` selects target authors; other replies become discussion context. With no filter, the selected export is the declared subject's evidence. The user must choose the collection deliberately. `--subject reviewer|team` records the intended profile subject. Identifying author/source mappings are written separately as private provenance. Comment prose can still contain identifying information; this split is not anonymization.

After `distill prepare --history FILE --style none|general`, return this draft shape:

```json
{
  "request_digest": "copy the request digest",
  "name": "Neutral descriptive profile name",
  "principles": [{
    "id": "resource-lifetime",
    "principle": "A newly inferred concern, not a copied comment",
    "applies_when": "The concrete conditions under which it matters",
    "rationale": "Why this concern affects correctness",
    "evidence_ids": ["an E- ID from this request"],
    "uncertainties": ["A limitation or competing interpretation, when applicable"]
  }],
  "limitations": ["Scope and evidence limitations"],
  "style": null
}
```

When general style was requested, `style` may instead contain `preferences: [strings]` and `evidence_ids: [E- IDs]`. Generalize verbosity or explanation structure, never identity, distinctive phrasing, or personality. Each principle needs target-role support. Human inspection remains necessary; schema and phrase checks cannot prove a profile is safe or faithful.

After `review prepare`, return:

```json
{
  "request_digest": "copy the request digest",
  "run": {"kind": "assistant", "host": "reported host or unknown", "model": "reported model or unknown", "isolation": "shared-session or fresh-session or unknown"},
  "reviewers": [{
    "id": "copy reviewer_id from the task",
    "status": "ok",
    "findings": [{"path": "src/example.py", "line": 3, "rule": "a-stable-issue-name", "severity": "high", "message": "The defect, triggering conditions and consequence", "principle_ids": ["a profile principle ID"], "context_evidence_ids": ["a captured C- ID"], "requires_context": true}]
  }]
}
```

Use `status: failed`, `findings: []` and an optional error explanation if a reviewer cannot complete. Every expected reviewer must be represented or the report is partial. `principle_ids` is empty for generic review; use only the selected profile's IDs otherwise. `context_evidence_ids` may be empty for change-only issues, with `requires_context: false`. Findings must be on added/replaced lines. Deletion-only issues cannot currently be anchored. Well-formed findings can still be wrong.

`review finalize` writes JSON plus escaped Markdown. It rejects invalid findings individually and exits 2 for partial results. Read failures, rejected counts, context gaps, outside-domain changes and change-collection gaps; do not equate zero findings with correctness.
