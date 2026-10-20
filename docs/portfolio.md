# Portfolio summary

I designed and built the original AI code review project alone, with AI assistance. My responsibilities included the overall architecture, distilling reviewer personas from historical review discussions, the evaluation and benchmark approach, and a test harness for ablations against generic review skills and prompts. This is my account of my role; private implementation evidence is not published.

The motivation was to turn recurring reviewer concerns into inspectable review instructions and evaluate their effect instead of assuming a generic prompt captures every relevant priority.

This repository is a newly authored public reconstruction. Users can supply eligible examples, ask their current assistant to derive a profile, inspect and save it, and apply it to changes with whole-codebase or selected-code-domain context. Shared helpers validate evidence references, changed-line findings and attribution. The evaluation harness pairs inputs for generic/persona and context/style comparisons.

The fictional worked example shows different learned concerns changing review emphasis on the same patch. It was created in the authoring assistant session, which knew the intended concerns. It is not independent evidence of improved quality. Native helper tests establish specific artifact, context and installation behavior; platform and live integration limitations are recorded separately.

No historical performance, cost, productivity, dataset-size or reviewer-activity figures are presented. New results are labeled synthetic and bounded by their test design. Original incidents, chronology, prompts, code and confidential implementation ancestry are omitted. The existing public repository setup history is retained.
