# Product brief

## Objective

Help users get accurate answers to support questions in their preferred language, with a clear path to a human when the agent cannot safely resolve the request.

## Proposed MVP

- Accept a support question and optional language preference.
- Identify the language when no preference is given.
- Retrieve relevant information from an approved knowledge base.
- Answer in the user's preferred language and cite supporting knowledge.
- Ask for clarification or hand off when information is missing.

## Decisions to make

- Target users, support domain, and initial supported languages.
- Knowledge sources, update process, and content ownership.
- Model provider, budget, hosting, and response-time targets.
- Escalation destination and human support workflow.
- Data retention and handling of personal information.

## Evaluation plan

Build a small synthetic evaluation set for each supported language. Review factual correctness, source support, language quality, appropriate escalation, latency, and cost. Define acceptance thresholds before a pilot.
