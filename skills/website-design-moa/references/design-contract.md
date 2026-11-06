# Website Design MOA contracts

Return exactly one JSON object without Markdown fences. The matching personal
agent definition is authoritative for the detailed allowed values.

## Specialist contract

UX, visual, and conversion specialists share this shape:

```json
{
  "specialist": "ux | visual | conversion",
  "status": "READY | PARTIAL | INCONCLUSIVE",
  "summary": "one concise sentence",
  "strengths": [
    {
      "claim": "observed strength",
      "evidence": [
        {
          "source": "file | render | brief | brand | analytics | research | measurement",
          "locator": "relative/path:line or page + viewport + element",
          "observation": "direct observation"
        }
      ]
    }
  ],
  "findings": [
    {
      "id": "role-prefixed stable ID",
      "severity": "critical | high | medium | low",
      "area": "role-specific area",
      "problem": "specific observed problem",
      "user_impact": "role-specific impact field",
      "evidence": [
        {
          "source": "evidence source",
          "locator": "concrete locator",
          "observation": "direct observation"
        }
      ],
      "recommendation": "design-level recommendation",
      "acceptance_checks": ["observable condition"],
      "confidence": "high | medium | low"
    }
  ],
  "coverage": {
    "inspected": ["actually inspected item"],
    "not_inspected": ["relevant uninspected item"]
  },
  "gaps": ["missing evidence or unresolved decision"]
}
```

The impact field is `user_impact` for UX, `design_impact` for visual, and
`business_and_user_impact` for conversion. `READY` requires concrete evidence,
representative desktop and mobile coverage, and at least one supported strength
or finding. `PARTIAL` requires explicit coverage gaps. `INCONCLUSIVE` is used
when the evidence cannot support reliable judgment.

## Director contract

```json
{
  "director": "site-design-director",
  "status": "READY | PARTIAL | INCONCLUSIVE",
  "summary": "one concise synthesis",
  "input_integrity": {
    "ux": "valid | partial | invalid | missing",
    "visual": "valid | partial | invalid | missing",
    "conversion": "valid | partial | invalid | missing"
  },
  "design_spec": {
    "intent": "single evidence-backed design intent",
    "principles": ["project-specific principle"],
    "priorities": [
      {
        "rank": 1,
        "id": "DS-1",
        "decision": "specific design decision",
        "rationale": "evidence-weighted reason",
        "source_findings": ["UX-1", "VIS-1", "CONV-1"],
        "evidence": [
          {
            "source": "evidence source",
            "locator": "concrete locator",
            "observation": "direct observation"
          }
        ],
        "scope": ["affected page, flow, viewport, or component family"],
        "acceptance_checks": ["observable condition"],
        "dependencies": ["decision, content, asset, or validation dependency"],
        "confidence": "high | medium | low"
      }
    ],
    "system": {
      "information_architecture": ["structural rule"],
      "journeys_and_interactions": ["journey or interaction rule"],
      "responsive_behavior": ["desktop/mobile adaptation rule"],
      "art_direction": ["project-specific visual direction"],
      "typography_color_grid": ["visual-system rule"],
      "component_language": ["component and state rule"],
      "content_cta_trust": ["content, CTA, and proof rule"],
      "accessibility_performance": ["verifiable constraint"]
    }
  },
  "conflicts_resolved": [
    {
      "topic": "conflicted decision",
      "positions": ["specialist position and finding ID"],
      "resolution": "chosen constraint, sequence, or experiment",
      "reason": "evidence-based reason"
    }
  ],
  "gaps": [
    {
      "missing": "required evidence",
      "blocks": ["affected design-spec IDs or system areas"],
      "next_evidence": "smallest evidence needed"
    }
  ],
  "validation_plan": ["desktop/mobile, state, accessibility, or performance check"],
  "authorization": "REPORT_ONLY"
}
```

The director receives all three normalized results and the original evidence.
It resolves conflicts by evidence strength, domain relevance, user impact,
confidence, dependency, and reversibility—not by vote count. `READY` requires
three valid inputs and one coherent design specification. `PARTIAL` names every
material constraint. `INCONCLUSIVE` is mandatory for missing or invalid inputs.
`authorization` is always `REPORT_ONLY`; implementation authority comes only
from the user's separate explicit request.
