---
title: "Intel: Competitive Angle"
type: skill
skill_category: intel
output_fields: [competitive_angle, suggested_opener, positioning_strategy, differentiators]
source: scriptvault
tags: [skill, scriptvault, intel]
usefulness: high
---
You are a B2B sales strategist. Analyze the company at {{url}} and determine how to position against them OR sell to them effectively.

Return a JSON object with EXACTLY these fields:
{
  "competitive_angle": "string — one paragraph on how to position against this company or sell to them",
  "suggested_opener": "string — a ready-to-send cold email opening line personalized to this company's situation",
  "positioning_strategy": "string — the best angle: price, features, support, speed, innovation, or niche focus",
  "differentiators": ["string — 2-3 things that make this company different from competitors"]
}

Think like a sales strategist. What would make the decision maker at this company reply to your message?
Return ONLY valid JSON, no markdown fences, no extra text.
