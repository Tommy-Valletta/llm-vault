# The complete assistant-guided workflow

The installed skill wraps these steps. The CLI is also available for inspection and automation of file handling. It does not supply AI reasoning. Use `python3` instead of `python` on macOS where appropriate. Put every private output outside your Git checkout; the examples below use a directory beneath your home folder.

## 1. Select and import examples

Choose a reviewer or team and only sources you are permitted to process with the current assistant. Local JSONL/JSON records contain comment text and optional author/thread/code context. Supported GitHub/GitLab JSON export shapes are described in the skill source reference. Use an existing connector or authenticated command to acquire remote examples; missing access is explained, not installed automatically. Record any collection limits or missing pages.

```text
python -m reviewbench history import --input examples/ownership-history.jsonl --reviewer fictional-author --permitted --out "$HOME/.llm-vault/tutorial/history.json"
python -m reviewbench distill prepare --history "$HOME/.llm-vault/tutorial/history.json" --style none --out "$HOME/.llm-vault/tutorial/distillation-request.json"
```

`--permitted` acknowledges processing authorization, not publication rights. Use `--subject team` for a deliberately selected team export. Other authors' replies remain discussion evidence. Identifying source mappings are saved in a separate provenance file; comment text can still contain identifying information.

## 2. Distill, inspect and save

Ask the invoking assistant to read the prepared request and write a draft matching the artifact reference. It should infer principles with applicability, rationale, source IDs and uncertainty. Choose `--style general` instead of `none` if you want broad style preferences. Review the draft before acceptance.

```text
python -m reviewbench distill finalize --request "$HOME/.llm-vault/tutorial/distillation-request.json" --draft "$HOME/.llm-vault/tutorial/draft.json" --accept-draft --out "$HOME/.llm-vault/tutorial/persona.json"
```

The helper validates structure, evidence IDs and exact long-phrase copying. These checks do not prove faithful inference, permission, confidentiality or absence of paraphrase.

## 3. Capture a change and context

For a local repository, use `review prepare --repo PATH --base HEAD --profile PROFILE`. It compares tracked working-tree/index changes with the base, without checkout, external diff or text conversion. Stage intended new files first; untracked exclusions are reported. It does not run target tests or code.

For the complete fictional remote-style export:

```text
python -m reviewbench review prepare --changes examples/changes.json --profile "$HOME/.llm-vault/tutorial/persona.json" --context codebase --source-snapshot examples/source-snapshot.json --context-selections examples/context-selections.json --out "$HOME/.llm-vault/tutorial/review-request.json"
```

Repeat `--profile` for multiple personas. Use `--generic` without profiles for a generic reviewer. See context.md for domain and existing-index options. Neither mode silently removes changed files from the review target.

## 4. Review and finalize

The current assistant reads each task and returns its attributed findings as response JSON. It must ground repository claims in the captured evidence and report uncertainty where evidence is absent. Stored outputs are labeled replay; actual assistant work is labeled assistant, with honestly reported host/model/isolation.

```text
python -m reviewbench review finalize --request "$HOME/.llm-vault/tutorial/review-request.json" --response "$HOME/.llm-vault/tutorial/response.json" --out "$HOME/.llm-vault/tutorial/report.json"
```

Read the JSON and Markdown reports, including failures, rejected outputs and retrieval gaps. Exit 2 can accompany a partial report; do not retry blindly or call it a clean review. Existing output files are never overwritten. Commands without `--out` use a new directory under the private default workspace. Set `LLM_VAULT_WORKSPACE` to choose another private parent.

The recorded synthetic requests/drafts/profiles/responses/reports demonstrate these formats. They can be inspected or replayed, but replay is not a new AI review or new distillation.
