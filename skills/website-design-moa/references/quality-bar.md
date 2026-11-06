# Website Design MOA — quality bar

Use this bar to evaluate the three specialist reports and the director's final
specification. A claim without a concrete locator is a gap, not a finding.

## Required evidence

- Record the exact page or flow, viewport, state, and visible element for every
  rendered observation; use `relative/path:line` for code evidence.
- Inspect at least one representative desktop viewport and one representative
  mobile viewport. Mark tablet and intermediate widths uninspected unless they
  were actually checked.
- Capture strengths as well as defects. Distinguish observed facts,
  recommendations, assumptions, and measurements still required.
- A final priority must trace to one or more specialist finding IDs and retain
  the supporting evidence.

## Experience checks

- **Journey and hierarchy:** the primary audience, promise, next action, and
  decision sequence are understandable without relying on decoration.
- **Responsive behavior:** content order, navigation, CTA visibility, type,
  media, grids, tables, overlays, and touch targets work on desktop and mobile
  without clipping, accidental overflow, or hidden essential actions.
- **States:** specify and inspect relevant default, hover, focus, active,
  selected, loading, empty, error, success, disabled, validation, and offline
  states. Do not invent states that the product cannot enter.
- **Content and trust:** copy is specific, truthful, scannable, and consistent;
  CTAs describe the resulting action; proof is attributable; no fake customer,
  certification, urgency, metric, guarantee, or business fact is introduced.

## Accessibility and performance checks

- Target WCAG AA: semantic structure, keyboard operation, visible focus,
  meaningful labels and alternatives, sufficient contrast, predictable
  interaction, clear errors, reduced-motion behavior, and zoom/reflow. Mark
  anything not directly tested as pending validation.
- Define a performance budget appropriate to the project. At minimum inspect
  image sizing and formats, font loading, above-the-fold payload, layout shift,
  animation cost, third-party scripts, and loading feedback. Do not infer field
  performance from appearance alone.

## Visual-system checks

- Art direction, typography, color, grid, spacing, imagery, and component
  language express the product and audience consistently across the inspected
  pages and both desktop and mobile.
- Favor a small number of intentional visual rules over accumulated effects.
  Originality must improve recognition or communication without weakening
  usability.
- Reject generic AI-site defaults when they lack a product-specific reason:
  interchangeable gradient heroes, glass cards everywhere, arbitrary glows and
  blobs, uniform rounded-card grids, meaningless metric tiles, fake social
  proof, stock slogans, and decoration that competes with content.

## Director gate

- All three specialist JSON results are present, valid, and refer to the same
  subject and evidence set before the director runs.
- The director resolves conflicts by evidence strength, domain relevance, user
  impact, confidence, dependencies, and reversibility—not by majority vote.
- The result is one ranked design specification with acceptance checks,
  explicit gaps, and a desktop/mobile validation plan.
- The final authorization remains `REPORT_ONLY`; implementation requires a
  separate, explicit user request.
