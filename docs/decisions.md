# Reconstruction decisions

These notes describe decisions made for this public reconstruction. They are not a historical development diary.

## Use synthetic concern labels

The history fixture supplies simple labels and original fictional lessons. The compiler uses a fixed concern catalog rather than learning personalities from prose. This demonstrates provenance and persona handling while making no claim to reproduce how historical reviewers think.

## Keep an offline baseline behind a reviewer interface

A deterministic backend makes expected behavior inspectable and avoids sending source to a provider. It checks a few Python constructs and cannot stand in for contextual AI review. The interface preserves a place for a future independently evaluated backend.

## Make context explicit

The caller supplies a fictional logging policy. Paired fixtures show that the same logging expression is treated differently with and without this policy. No context is inferred from private examples or fetched from another system.

## Prefer exact duplicate handling

File, line, and rule form a transparent identity. This avoids making unsupported claims about semantic consensus, while exposing the tradeoff that different rule identifiers will not merge even when they describe the same issue.

## Publish reproducible new evidence

The tests exercise scope filtering, adapter validation, attribution, context dependence, and common baseline false positives. The regression cases were authored alongside the rules. Perfect performance on these fixtures would establish agreement with those expectations, not general review quality.

## Lessons the design makes visible

Persona diversity is useful only if requests, outputs, and evidence can be inspected. Context should have an explicit entry point. Aggregation should retain attribution without counting agreement as truth. Evaluation needs negative cases and honest boundaries around what a score means. These are design explanations, not accounts of specific historical incidents or measured improvements.
