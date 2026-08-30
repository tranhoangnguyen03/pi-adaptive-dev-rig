# Research landscape

This is a working research brief, not an endorsement list. Claims about external projects require direct verification before citation, adoption, or code reuse.

## Provenance

| Source | Checked | Evidence status |
|---|---:|---|
| Anthropic context-engineering article | 2026-08-28 | Directly read from published URL |
| Scott Fryxell article | 2026-08-28 | Directly read from published URL |
| coctostan/pi-superpowers | 2026-08-28 | Local source and README inspected; local revision to be pinned before evaluation |
| pcvelz/superpowers | 2026-08-28 | Repository README inspected via GitHub API |
| PiLastDigit/TRIP-workflow | 2026-08-28 | Repository README inspected via GitHub API |
| friedbotstudio/baseline | 2026-08-28 | Repository README inspected via GitHub API |
| Section 3 follow-up candidates | 2026-08-28 | Mixed: scout reports or README-level review; each item requires source/license validation before use |

Before an evaluation or implementation depends on a source, record its repository URL, exact commit/version, date checked, license, and the specific verified claim.

## 1. Primary influences

### Anthropic — The new rules of context engineering for Claude 5 generation models

https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models

Pertinent shifts:

- rules → model judgment;
- examples → expressive interface design;
- put everything upfront → progressive disclosure;
- repeated instructions → simple tool descriptions;
- heavy memory files → selective memory and references;
- simple prose specs → rich references such as code, tests, artifacts, and rubrics.

Implication: keep the portable posture header small; expose detailed capability guidance only when needed; encode important constraints in interfaces and executable systems rather than repeated prose.

### Scott Fryxell — The Harness Is the Thing

https://scott-fryxell.github.io/blog/the-harness-is-the-thing/

Pertinent ideas:

- the durable asset is the user-owned harness, not one model vendor or TUI;
- shared skills and `AGENTS.md` can unify model experiences;
- harness as jig: support skilled work rather than prescribe every motion;
- repeated reasoning should become scripts/tools that can run without recurring token cost;
- artifacts should be auditable and have intentional destinations;
- planner/worker/critic/promoter and model routing can help when objectives conflict, but are personal adaptations rather than universal law;
- early skills can be too prescriptive; simplification should be empirical.

Implication: maintain a portable skills/scripts/evaluation layer and a thin Pi-specific runtime layer. Borrow the customization principle, not Fryxell's exact five-stage workflow.

## 2. Baseline and known candidates

### coctostan/pi-superpowers

https://github.com/coctostan/pi-superpowers

Role in this project:

- high-value source material;
- current comparison baseline;
- example of Pi-native package and branch-aware tool state;
- example of process coupling and mandatory-language failure modes.

Strong material to retain selectively:

- root-cause debugging;
- evidence-before-claims;
- test-design knowledge;
- review rubrics;
- worktree safety;
- destructive finish confirmations;
- skill validation.

### pcvelz/superpowers

https://github.com/pcvelz/superpowers

Claude Code-specific extension of Superpowers using native tasks, metadata, routing, and hook enforcement. It adds control rather than reducing ceremony. Useful as a governance and task-enforcement reference, not the lightweight default.

### PiLastDigit/TRIP-workflow

https://github.com/PiLastDigit/TRIP-workflow

Minimal public flow: Plan → Implement → Release. Useful as a simplicity benchmark and cross-tool Agent Skills example. Its central `ARCHI.md` and fixed lifecycle may conflict with progressive disclosure and fast-changing prototypes.

### friedbotstudio/baseline

https://github.com/friedbotstudio/baseline

A production governance layer with numerous hooks, skills, workflow tracks, and out-of-model consent gates. Useful for studying genuine tool-boundary authorization. Too heavy as the everyday Prototype/Standard model.

## 3. Unverified or partially verified follow-up leads

These were surfaced by independent Claude, Codex, and Antigravity scouts. Treat descriptions as leads, not facts, until the repository, implementation, activity, license, and relevant claim are checked directly.

### Agent Skills specification and Anthropic skills

- https://github.com/agentskills/agentskills
- https://github.com/anthropics/skills

Why relevant:

- metadata-first discovery;
- model-driven activation;
- focused references/scripts loaded on demand;
- skill-trigger and baseline-vs-skill evaluation tooling.

Likely disposition: adopt the portable format and evaluation ideas.

### Pi native primitives

Primary Pi documentation was read during design. It documents skill progressive disclosure, custom session entries, active-branch reconstruction through session APIs, status UI, `before_agent_start`, compaction hooks, tool interception, and dynamic tool loading.

Why relevant: Pi appears to supply the runtime needed for a later posture-state experiment. Exact installed-version behavior must be pinned and tested; do not add a workflow engine.

### coctostan/pi-superpowers-plus

Scout-reported claim: moves detail into on-demand references and runtime monitoring. Verify the canonical repository, source diff, license, and maintenance status before relying on this description.

### EveryInc/compound-engineering-plugin

https://github.com/EveryInc/compound-engineering-plugin

Reported useful concepts:

- conditional planning;
- self-sizing review;
- confidence anchors;
- independent reviewers before corroboration;
- non-mutating review defaults.

Likely disposition: borrow selectively; full pipeline may remain too prescriptive.

### HumanLayer advanced context engineering

https://github.com/humanlayer/advanced-context-engineering-for-coding-agents

Useful for difficult/hardened work:

- intentional context management;
- research → plan → implement when warranted;
- durable artifacts between long phases;
- human attention concentrated at high-leverage decisions.

License must be checked before copying content.

### Habitat-Thinking/ai-literacy-superpowers

Scout-reported claim: three enforcement loops—advisory edit-time, stricter PR-time, and scheduled investigative audit. Verify the canonical repository, actual implementation, license, and activity.

### Gemini CLI and OpenCode permission models

- https://github.com/google-gemini/gemini-cli
- https://github.com/anomalyco/opencode

Useful concepts:

- allow / deny / ask-user effects;
- scoped rule precedence;
- parent/subagent permission consistency;
- explicit plan/build distinctions.

Borrow policy vocabulary and recursive-gate lessons, not their engines.

### Selected Pi extensions

Reported candidates in `emanuelcasco/pi-mono-extensions`:

- bounded context reads;
- duplicate-read suppression;
- secret scanning;
- write→execute correlation;
- review findings with explicit UI.

Install or copy nothing before direct code/security review.

### Promptfoo and Anthropic skill evaluation

- https://github.com/promptfoo/promptfoo
- Anthropic `skill-creator`

Useful for:

- baseline comparisons;
- multi-model scenario runs;
- hidden and weighted assertions;
- trigger and near-miss tests;
- timing/token comparison;
- qualitative review.

Pi integration requires validation or a small adapter.

### Cisco Skill Scanner

https://github.com/cisco-ai-defense/skill-scanner

Potential optional Hardened check for third-party skill ingestion. Not an everyday runtime dependency.

### AGENTS.md standard and portable config patterns

- https://github.com/agentsmd/agents.md
- portable skill/config synchronization projects

Useful for maintaining a cross-TUI harness layer. Do not assume symlink or config-sharing schemes are turnkey.

### Aider architect/editor and repository-map patterns

https://github.com/Aider-AI/aider

Useful principles:

- executable compiler/test feedback;
- structural repository maps;
- role separation when planning and editing objectives conflict;
- git-native checkpoints.

## 4. Full-process references, not defaults

These may inform Hardened posture or comparison baselines:

- GitHub Spec Kit: https://github.com/github/spec-kit
- BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD
- Baseline governance
- Ralph-style autonomous loops and circuit breakers
- HumanLayer advanced context engineering

They should not be adopted wholesale merely because they are comprehensive.

## 5. Anti-patterns to avoid

- injecting the whole methodology into every session;
- repeating universal negative constraints in multiple prompt layers;
- examples that constrain frontier models to one exploration path;
- all-or-nothing process rigor;
- forced documents without a consumer;
- stale architecture or memory files competing with code;
- unnecessary subagent fan-out;
- governance that exists only as model-readable prose when a true boundary is required;
- broad deterministic classifiers for semantic judgments;
- cross-tool portability claims without testing;
- copying unlicensed material;
- treating reviewer agreement as stronger than executable evidence;
- measuring compliance with the framework instead of delivery outcomes.

## 6. Verification backlog

Before relying on a candidate:

- verify canonical repository and current activity;
- inspect actual source rather than README claims;
- verify license compatibility;
- measure always-on prompt and tool-schema cost;
- test Pi compatibility against the installed Pi API/version;
- examine hook behavior for parent and delegated agents;
- assess maintenance and security burden;
- compare against a smaller local implementation;
- validate claimed evaluation results.
