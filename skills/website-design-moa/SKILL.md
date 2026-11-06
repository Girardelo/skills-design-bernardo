---
name: website-design-moa
description: >-
  Orchestrate a multi-agent website-design team only when the user explicitly
  names website-design-moa or asks for the equipe de interfaces, especialistas
  de interface, departamento de produto e interfaces, or agentes de interface.
  Generic website, landing page, ecommerce, dashboard, portal, and web-app
  design work stays with the main agent. Do not use for a narrow frontend bug,
  backend-only work, or a general repository review.
---

# Website Design MOA

## Explicit activation

Do not activate this department from generic phrases such as `revise o design
do site`, `crie o design do site` or `melhore o design do site`. The user must
explicitly ask for this workflow or its interface team.

Turn one website brief or existing interface into one evidence-backed design
direction. Run three specialists independently, then let a design director
resolve their conflicts into a single specification. Do not average opinions or
present three disconnected concepts as the final answer.

## Select the mode

Choose exactly one mode from the user's wording:

- `review`: `Revise o design do site`. Inspect and report only; never edit the
  repository or production system.
- `concept`: `Crie o design do site: <brief>`. Produce a design specification,
  content hierarchy, responsive behavior, and optional visual exploration; do
  not infer authorization to implement code.
- `implement`: `Melhore o design do site` or an explicit request to implement
  the approved design. Apply local changes and validate them, but never commit,
  push, deploy, publish, or change production configuration.

The three design specialists always run in parallel. If the user also says
`faz em paralelo`, apply that command to the later code implementation through
`$parallel-implementation`; do not create a second competing design team.

When the user asks to create a complete web project, let `$project-create-moa`
own destination safety, Git initialization, and project promotion. Use this
skill as its design stage. When the user asks to review the whole repository
rather than the experience, let `$project-review-moa` own the review.

## Establish evidence

For an existing repository, read every applicable `AGENTS.md`, then run:

```sh
python3 <skill-dir>/scripts/design_moa.py preflight \
  --repo <repository-root> --output <temp-dir>/design-preflight.json
```

The preflight is the source of truth for Git state, instructions, framework,
package manager, pages, components, styles, tokens, assets, and available
test/build commands. Keep durable artifacts outside the repository.

Collect the smallest useful visual evidence:

- existing runnable site: inspect the rendered interface at representative
  desktop and mobile widths, plus the key state or journey named by the user;
- supplied URL: use browser control and the current authenticated session when
  required, without mutating external state;
- screenshot or mockup: inspect it directly and record what cannot be inferred;
- greenfield brief: use provided brand assets and audience facts; label all
  missing business context as assumptions.

Never claim visual inspection from source code alone. Never invent user
research, conversion data, brand rules, accessibility scores, or competitor
facts. Read [references/quality-bar.md](references/quality-bar.md) before visual
judgment and [references/design-contract.md](references/design-contract.md)
before delegating.

## Run three specialists in parallel

Spawn exactly three independent read-only specialists concurrently. Give all
three the same brief, preflight, screenshots, applicable instructions, and
contract. Do not pass one specialist's conclusions to another.

1. `site-design-ux`: information architecture, journey, hierarchy, interaction,
   component behavior, states, and responsive structure.
2. `site-design-visual`: art direction, typography, color, grid, spacing,
   imagery, component language, brand fit, and avoidance of generic AI styling.
3. `site-design-conversion`: message hierarchy, content, calls to action,
   trust, accessibility, performance perception, and conversion friction.

Use the personal agents when available; otherwise give ordinary subagents the
same role instructions. Specialists remain read-only even in `implement` mode.
Normalize every response:

```sh
python3 <skill-dir>/scripts/design_moa.py normalize \
  --role ux --input <raw.json> --output <normalized.json>
```

Use `visual` and `conversion` for the other roles. Timeout, invalid JSON,
missing evidence, or contract failure becomes `INCONCLUSIVE`; never translate
it into approval. Retry an inconclusive role once in a fresh context only when
the failure was timeout or malformed output.

## Run the design director afterward

Only after all three normalized results exist, spawn `site-design-director` in
a fresh read-only context. Give it the evidence bundle and require one director
contract. The director must:

- distinguish observed facts, design judgment, and assumptions;
- resolve conflicts by user goal, evidence, accessibility, and feasibility;
- produce one design thesis and one prioritized direction;
- retain explicit desktop and mobile behavior;
- define tokens and components precisely enough to implement;
- mark unsupported areas `PARTIAL` or `INCONCLUSIVE`;
- reject vague language such as `clean`, `modern`, or `premium` unless followed
  by concrete visual decisions.

Normalize with `--role director`. The director is not an implementation
authorization and may not edit the repository.

## Deliver by mode

### Review

Return the highest-impact findings, evidence, affected viewport or journey,
recommended correction, and acceptance criterion. Include inspected and
uninspected pages/states. Do not change code.

### Concept

Return a single design specification containing:

- audience, job, and design thesis;
- page or journey structure;
- section-level content hierarchy;
- responsive layout and interaction rules;
- typography, color, spacing, radius, elevation, and motion tokens;
- component and state inventory;
- imagery or illustration direction;
- accessibility and performance constraints;
- prioritized implementation sequence and measurable acceptance criteria.

Generate visual concepts only when they materially improve the decision. Label
them as direction, not as validated production design.

### Implement

Treat the director specification as the implementation contract. Before edits,
state the pages/components in scope and preserve existing behavior not named by
the contract. Use the most relevant frontend/product-design skill available.
Enter `$parallel-implementation` only when explicitly requested or when its
gate approves a genuinely high-risk, multi-file implementation.

After implementation:

1. run the repository's structured lint, typecheck, test, and build commands;
2. render the changed experience at desktop and mobile widths;
3. exercise important hover, focus, loading, empty, error, and success states;
4. give the before/after evidence and original contract to a fresh read-only
   design-director context for final sign-off;
5. compare the sign-off against the director contract and quality bar;
6. correct material regressions and repeat validation.

Do not declare success from a build alone. If rendering is unavailable, report
the visual validation as incomplete rather than guessing.

## Persist the design run

Write a concise report in the user's language, then persist outside the
repository:

```sh
python3 <skill-dir>/scripts/design_moa.py create-run \
  --preflight <preflight.json> \
  --ux <ux.json> --visual <visual.json> --conversion <conversion.json> \
  --director <director.json> --report <report.md>
```

The run belongs under `~/.codex/design-runs/<run-id>/` and must contain the
preflight, three normalized specialist results, director result, and report.
Report its absolute path. Never store generated reports, screenshots, or agent
transcripts inside the target repository unless the user explicitly requests a
project asset.
