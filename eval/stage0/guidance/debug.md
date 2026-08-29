---
name: debug
description: Reproduce first, test the leading hypothesis, fix the shared root cause instead of the symptom — and audit sibling callers. Load when investigating any failure.
---

# Debug

1. Reproduce the failure with the smallest concrete input before theorizing.
   A failure you cannot reproduce is a hypothesis, not a fact.
2. State the leading hypothesis, then test it directly — instrument, bisect,
   or minimize until confirmed or replaced.
3. When confirmed, fix the root cause where it lives, not where the symptom
   surfaced. Before editing a shared function or helper:
   - list every caller (`grep` the symbol), and
   - check whether the same defect reaches them too.
   A special case in one caller leaves every sibling caller broken.
4. Protect the fix: add or strengthen a test that fails on the original
   defect and passes after the fix.
5. Distinguish verified facts from assumptions in every status report.
   Cite the command or test output that settled each question.
