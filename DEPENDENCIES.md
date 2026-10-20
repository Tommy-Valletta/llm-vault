# Dependencies, licensing and provenance

Runtime: Python 3.11+ standard library. Git is an optional external executable required for local Git reviews. Existing gh/glab or session connectors are optional access routes; their presence does not prove authorization. The user obtains Python/Git/host tooling separately under their own licenses. No private package, model SDK, indexer, embedding dependency, vendored implementation, or runtime dependency installation is required.

Source-run CLI: `python -m reviewbench`. There is no PyPI release or installer build backend. `skill install` copies the canonical Python source, skill resources and synthetic baseline fixtures into a self-contained local skill with an installation manifest. It does not install third-party packages, change host configuration or configure accounts.

The reconstruction's source, skill prompts, docs and examples are newly authored. Recorded histories, profiles, requests and responses are explicitly synthetic. Existing public setup ancestry and its license are retained; confidential implementation ancestry is excluded. The MIT grant covers new reconstruction material only, not original private code, prompts, datasets or operational evidence.

Development may use an external skill validator requiring a separately installed YAML parser; neither that validator nor its dependencies are included in the runtime or redistributed. Raw runtime artifacts and private review records do not belong in the publication manifest.
