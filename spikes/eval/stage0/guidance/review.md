---
name: review
description: Self-review the diff against the claim before delivering; use independent review only for judgment gaps executable evidence cannot settle. Load when checking work before handoff.
---

# Review

1. Re-read the full diff before claiming done. For each hunk ask: does this
   serve the named criteria, or is it scaffolding the claim does not need?
2. Check the delivery claim against the evidence:
   - every named criterion preserved or explicitly renegotiated;
   - facts distinguished from assumptions;
   - fresh evidence cited for each success statement;
   - residual limitations and untested scope named.
3. Hunt the classic misses: sibling callers of changed shared code, error
   paths, boundary values, deleted-or-bypassed assertions, debug leftovers.
4. Independent review earns its cost only when a material judgment remains
   that executable evidence cannot settle. Name that gap if you use it;
   otherwise self-review is enough.
5. Disclose what a reviewer or maintainer will trip over next — unknowns,
   temporary hacks, deferred edge cases — instead of leaving them to be
   discovered.
