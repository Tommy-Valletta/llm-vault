# LLM Vault — distill a reviewer, then review with it

Turn permitted review examples into an inspectable persona, then apply its priorities to a code change with scoped source evidence. The reusable skill uses the AI assistant you already have open. Python helpers capture inputs, validate outputs, retain attribution, and prepare comparisons; they do not secretly call another model.

## Current validation status

The native Mac run completed the synthetic distillation, user acceptance, profile save/reload and contextual review workflow. After correcting a test assertion to compare canonical paths, the Mac helper suite passed **all 32 tests, with no skips**. Windows passed 31 tests with one host-dependent symlink test skipped. A new Mac assistant chat discovered the installed skill from its initial catalogue and ran its doctor helper successfully. The full workflow was exercised in the earlier Mac validation chat. See [validation status](docs/validation.md) for the observed evidence and limits.

## Why I built this

Generic review prompts do not express every concern a reviewer develops through repeated code review. My goal was to make those concerns explicit, reusable, and testable rather than rely on an assistant guessing a team's preferences.

I was the sole developer of the original project, with AI assistance. I designed its architecture, persona distillation pipeline, evaluations and benchmarks, and test harness for ablations against generic review skills and prompts. This is my account of that work; confidential implementation evidence and operational measurements are not published here.

This repository is a newly authored public reconstruction. It preserves the general engineering workflow using original prompts, fictional histories, and synthetic code. The existing public repository setup history is retained; confidential implementation history is not imported.

## What you can do

1. Supply examples you are permitted to process, from local files or selected GitHub/GitLab discussions using access tools available in your session.
2. Ask the skill to distill priorities and reasoning, optionally adding broad writing-style preferences. Inspect the evidence-linked draft and save a profile.
3. Review local Git changes or an accessible pull/merge request with one or more saved profiles.
4. Choose whole-codebase, selected-code-domain, or no surrounding context. Independently choose direct tools or an existing index.
5. Inspect attributed findings, captured source references, missing context and rejected outputs. Prepare generic/persona and context/style ablations.

The assistant performs the reasoning; the CLI alone does not infer a persona or run an unattended AI review. GitHub/GitLab/index availability depends on your existing session tools and permissions. No indexer, embedding service, authentication setup, or model API key is supplied.

## Start on Windows or macOS

You need Python 3.11+ and an AI coding assistant capable of local file/command use. Git is needed for local Git reviews; hosted source tools are optional. No third-party runtime packages are required.

```text
git clone https://github.com/Tommy-Valletta/llm-vault.git
cd llm-vault
```

Windows PowerShell:

```powershell
python -m reviewbench doctor
python -m reviewbench skill install --dest "$HOME/.agents/skills"
```

macOS terminal:

```sh
python3 -m reviewbench doctor
python3 -m reviewbench skill install --dest "$HOME/.agents/skills"
```

Use an available `py -3` launcher on Windows if `python` is unavailable. Choose `--dest` to match your host's skill discovery directory; older setups may use a different directory. Installation refuses to overwrite an existing skill. The installed skill contains its own copy of the canonical runtime and does not depend on the clone location.

Invoke `$persona-review` in your assistant, for example: “Distill a priorities-only persona from examples/ownership-history.jsonl, show me the draft, then review examples/changes.json with the supplied source snapshot and context selections.” The examples are explicitly fictional. Source data is visible to the invoking assistant; local helper execution does not mean local AI inference.

See the [complete workflow](docs/workflow.md) for command handoffs, [context options](docs/context.md), and [Windows/macOS acceptance](docs/platforms.md). The skill's [artifact reference](skills/persona-review/references/artifacts.md) documents draft and response JSON.

## Inspect a concrete result

The [synthetic worked example](examples/recorded/worked-example.json) contains two independently worded histories, their derived profiles, request packets and reviews. The ownership profile focuses on closing a borrowed channel. The compatibility profile focuses on a renamed keyword and a changed return structure. Both receive the same proposed change and source context.

These outputs were produced in the authoring assistant session and validated by Python. That session also authored the examples and knows their intended concerns. They demonstrate the workflow and different review emphasis, not independent accuracy or superiority to generic review.

## Engineering evidence

- Grounded profiles support arbitrary principles, source references, scope and uncertainty rather than a fixed tag catalog.
- Context capture separates selection scope from retrieval method, records gaps and rechecks indexed excerpts against accessible source.
- Finalization checks changed-line locations, persona/context IDs and attribution, rejects malformed findings, and preserves partial failures.
- Evaluation packets separate scoring material and hold change/context hashes constant for generic/persona comparisons.
- Native helper tests exercise installation, Unicode paths, the complete CLI handoff and synthetic replay cases. See [validation status](docs/validation.md) for exactly what has and has not been run.

The original AST demo remains as an explicitly limited baseline:

```text
python -m reviewbench demo
python -m reviewbench evaluate
python -m unittest discover -s tests -v
```

Use `python3` on macOS as appropriate. Those baseline fixture scores do not measure AI persona quality.

## Read further

[Architecture](docs/architecture.md) · [reconstruction decisions](docs/decisions.md) · [evaluation](docs/evaluation.md) · [limitations](docs/limitations.md) · [portfolio summary](docs/portfolio.md) · [dependencies](DEPENDENCIES.md)

Raw histories, profiles, provenance and reports are private by default and must remain outside Git. Do not use confidential material without the necessary processing permission, or assume a distilled profile is cleared for publication. No confidential project material is included. The MIT license applies to newly authored reconstruction material only; see [LICENSE](LICENSE). The exact candidate file list is [PUBLICATION_MANIFEST.json](PUBLICATION_MANIFEST.json).
