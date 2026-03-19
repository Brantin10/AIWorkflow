---
title: "Optimizer: Variant Generator"
type: skill
skill_category: optimizer
source: scriptvault
tags: [skill, scriptvault, optimizer]
---

# Optimizer: Variant Generator

Generates AI-powered variant skeletons from high-performing baselines, scores them on quality metrics, and tracks improvement across optimization rounds.

## Prompt

```
You are an expert B2B sales copywriter and A/B testing specialist.

Here are {n} high-performing sales script templates (skeletons) with their success metrics:

{baseline_examples}

Generate {num_variants} new variant templates that could OUTPERFORM the baselines.

For each variant:
1. Keep the same {{variable}} placeholders
2. Try a different angle: {angles}
3. Aim for higher reply rates

Return a JSON array of variants:
[
  {
    "title": "string - descriptive variant name",
    "angle": "string - what makes this variant different",
    "template_content": "string - the full template with {{variables}}",
    "reasoning": "string - why this might outperform the baseline"
  }
]

Return ONLY valid JSON, no markdown fences.
```

## Scoring Metrics (0-5 scale)

| Metric | What it measures |
|---|---|
| clarity | Sentence length, passive voice, adverb density |
| personalization | Variable count (3-5 ideal) |
| structure | Greeting, value prop, CTA, sign-off presence |
| urgency | Time-sensitive language (moderate = best) |
| social_proof | Numbers, proof keywords, testimonials |
| call_to_action | Action verbs and questions in closing |
| relevance | Industry-specific keyword density |
| conciseness | Word count (50-150 ideal) |

## API Endpoints

- `POST /api/v1/optimizer/generate` — Generate variants from baselines
- `POST /api/v1/optimizer/round` — Run optimization round (pick best, generate new)
- `GET /api/v1/optimizer/history/{variant_group}` — View all variants with scores
- `POST /api/v1/optimizer/score/{skeleton_id}` — Score a single skeleton

## Default Angles

- pain-point-led
- social-proof-led
- question-led
- urgency-led
