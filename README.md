# Reviewbench: a public reconstruction

Reviewbench demonstrates how a review engine can give several reviewers different concerns, supply explicit project context, and combine their findings into one report. All code, prompts, histories, and examples in this repository were newly authored for this reconstruction.

The motivation comes from work on an AI code review engine that used reviewer personas informed by past review discussions. This repository preserves the general orchestration idea. Its included backend is a deterministic Python syntax-tree baseline, not an AI model or a replica of an operational system. It makes the workflow runnable and testable without external accounts or services.

## Try it

Use Python 3.11 or newer from this directory. No installation, network connection, credentials, or third-party runtime packages are required.

```text
python -m reviewbench demo
python -m reviewbench evaluate
python -m unittest discover -s tests -v
```

The fictional Kite Board examples include dynamic evaluation, mutable default arguments, and logging of a field restricted by a synthetic policy. The combined example produces three actionable findings with after-file line numbers and reviewer attribution. Reviewed source is parsed as data and never executed.

## What this demonstrates

- Compile concern labels from explicitly synthetic history into new reviewer personas. Lesson text is not copied into system instructions.
- Select reviewers, construct separate instructions and input data, and pass a request to a replaceable reviewer interface.
- Supply an explicit context policy; the boundary check changes behavior when that policy is absent.
- Reject findings outside changed lines, combine exact duplicate issues, and preserve reviewer attribution.
- Run positive and negative synthetic regression fixtures with explicit expected findings.

The source is deliberately small. See [architecture](docs/architecture.md), [decisions](docs/decisions.md), [limitations](docs/limitations.md), [evaluation](docs/evaluation.md), and the [portfolio summary](docs/portfolio.md).

## Evidence and scope

All evaluation results produced here are new synthetic regression results. They say nothing about historical production quality, reviewer productivity, costs, or organizational activity. The fixtures were written with knowledge of the baseline rules; they are not an independent holdout dataset. No historical quantitative claim is made.

The public implementation demonstrates a general approach to orchestration. It does not independently establish authorship of every part of the earlier system or reproduce its complete behavior.

## Dependencies and license

The supported run commands use only Python's standard library. This is a source-run demonstration; no installable package or build process is supplied. There are no private packages, model SDKs, remote adapters, or vendored dependencies.

The MIT license covers the newly authored files in this reconstruction. The repository's earlier public setup commit is retained. No confidential project code, prompts, datasets, assets, or implementation history are imported. Python retains its own license. See [LICENSE](LICENSE) and [dependency notes](DEPENDENCIES.md).

The exact publication payload is recorded in [PUBLICATION_MANIFEST.json](PUBLICATION_MANIFEST.json).
