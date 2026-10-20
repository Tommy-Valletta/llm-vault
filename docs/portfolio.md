# Portfolio summary

I worked on an AI code review engine that used reviewer personas informed by past review discussions. The goal was to make reviews reflect several relevant concerns while supplying project context to the review process.

This repository is a fresh public reconstruction of that engineering approach. It demonstrates persona handling, structured review requests, explicit context, a replaceable reviewer interface, finding validation, duplicate handling, and reproducible evaluation using entirely synthetic examples.

The included reviewer is an offline deterministic baseline. Its purpose is to make the workflow concrete and inspectable, not to claim AI review quality. The tests demonstrate specific behavior of this reconstruction. No historical performance, productivity, cost, dataset, or reviewer-activity measurements are presented.

The engineering story is about making reviewer concerns explicit, defining the boundary between context and instructions, preserving attribution through aggregation, and evaluating findings against stated expectations. The reconstruction's decision notes explain the tradeoffs made here. Private incidents and an unsupported historical experiment timeline are omitted.
