---
name: explore-design
description: Frame the question and choose a relevant experiment or change shape before implementing. Load when scoping work, weighing alternatives, or deciding how deep to go.
---

# Explore / design

1. Name the question the work must answer and the criteria that will decide
   it. If they are already named (ticket, issue, user prompt), reuse them
   instead of re-deriving.
2. Read only the context the claim needs — trace the affected flow, not the
   whole repository. Prefer code, tests, and existing artifacts over prose.
3. Consider alternatives only when they are materially different in risk or
   cost. One good path plus a named rejected alternative is usually enough.
4. Choose the change shape: smallest convincing implementation for a
   prototype; repository-fit change with protected behavior for standard
   work; add analysis breadth only for consequential claims.
5. Write design notes only when a real future consumer exists (a PR
   description, a test, a script). Otherwise keep the design in the
   conversation.
6. Declare the delivery posture visibly when implementation starts, and say
   what the work will and will not establish.
