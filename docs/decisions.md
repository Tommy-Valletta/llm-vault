# Decisions for the public reconstruction

These describe the rebuild, not an invented diary of the original project.

## Use the invoking assistant

The skill uses capabilities and accounts already available in the user's session. Helpers prepare and validate artifacts; they do not manage model credentials or make hidden inference calls. This supports a portable workflow but does not promise unattended terminal operation or independent model execution.

## Distill principles from evidence

An explicit draft makes applicability, rationale, evidence and uncertainty inspectable. Broad style extraction is a per-distillation choice. Fixed concern tags remain only in the legacy baseline. Distilled material can remain sensitive; transforming it is not permission to publish it.

## Separate scope from retrieval

A selected controller/service is a code boundary. An index is a way to locate evidence within that boundary. Existing tools are sufficient for v1; building another index would add privacy and platform obligations without proving better retrieval. Source checks and explicit gaps matter more than provider labels.

## Preserve attribution without claiming consensus

Exact duplicate keys are transparent and reproducible. Every contributing reviewer retains its own principle/message attribution. Agreement is not correctness, and semantically related findings with different keys will not merge automatically.

## Evaluate controlled differences

Generic/persona requests share the captured change and context. Retrieval comparisons are separate. Judgments stay outside review packets. Recorded examples and replay tests make behavior inspectable but cannot establish independent AI quality. Scores need explicit adjudication, rationale and honest session/model metadata.

## Keep the public story precise

The original engineering contribution is owner-reported. Newly authored implementation and results are labeled reconstruction. Repository setup ancestry is preserved while confidential implementation history and operational measurements remain excluded.
