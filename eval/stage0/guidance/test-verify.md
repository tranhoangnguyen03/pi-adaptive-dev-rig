---
name: test-verify
description: Match evidence to the claim — smallest executable proof for prototypes, targeted regression protection for changed behavior, fresh cited evidence at completion. Load when deciding what proof a claim needs.
---

# Test / verify

1. Scale evidence to the claim:
   - Prototype: one runnable proof of the named criteria (script, demo,
     fixture, sample).
   - Standard: targeted regression protection for the behavior you changed,
     plus the repository's own relevant checks.
2. Design tests around behavior and failure modes, not line coverage.
   Cover the case that was wrong, the boundary next to it, and the sibling
   paths that share the code.
3. Run the real commands and cite the actual output. A prose summary is not
   evidence.
4. When a check is cheap to falsify, falsify it: run it once against known-bad
   input to confirm it can fail.
5. At completion, report fresh evidence only — produced by this change, not
   by earlier runs — and name what was deliberately not assessed.
