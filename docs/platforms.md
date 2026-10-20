# Windows and macOS acceptance

Python 3.11+ is required; Git is needed for local change capture. Core helpers use the standard library. Commands do not require Bash, WSL, a model API key, or an indexing service. Choose an interpreter that really exists; Windows Store aliases are not proof that Python is installed.

Install using the README commands. The installed skill includes its runtime and runs from an unrelated working directory. `--dest` chooses the parent skill directory and refuses to overwrite an existing installation. Tool discovery (`doctor`) reports executable presence only, not account authentication or connector access.

The candidate acceptance package contains only public-candidate source, tests and synthetic examples, with no .git directory, original bundle or private audit. After extracting it on a Mac:

```sh
python3 tools/acceptance.py --out "$HOME/.llm-vault/mac-acceptance.json"
python3 -m reviewbench skill install --dest "$HOME/.agents/skills"
```

The first command runs native helper tests, including a complete installed CLI journey using synthetic replay responses from a Unicode/space-containing temporary path. Keep its report private because test failures can reveal machine paths. Then start a fresh assistant session, invoke `$persona-review`, and perform the documented synthetic distillation/save/reload/contextual-review workflow. Confirm that the skill is discovered, instructions work without authoring-session assumptions, and missing optional tools are explained.

Record OS/Python versions and outcomes privately; do not add raw logs or machine paths to the public repository. A helper-test pass is distinct from actual assistant invocation and live source/index validation. See validation.md for the current evidence, which must not mark unrun Mac or fresh-session steps passed.
