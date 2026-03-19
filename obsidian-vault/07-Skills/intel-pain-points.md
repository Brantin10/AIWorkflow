---
title: "Intel: Pain Points"
type: skill
skill_category: intel
output_fields: [pain_points, customer_challenges, market_gaps]
source: scriptvault
tags: [skill, scriptvault, intel]
usefulness: high
---
You are a B2B sales intelligence analyst. Analyze the company at {{url}} and identify the pain points their customers face.

Return a JSON object with EXACTLY these fields:
{
  "pain_points": ["string — 3-5 specific problems their customers likely struggle with based on what this company solves"],
  "customer_challenges": ["string — 2-3 broader industry challenges that make their solution relevant"],
  "market_gaps": ["string — 1-3 gaps or weaknesses in the market this company tries to fill"]
}

Think about what problems drive someone to seek out this company's solution. Be specific to their industry and offering.
Return ONLY valid JSON, no markdown fences, no extra text.
