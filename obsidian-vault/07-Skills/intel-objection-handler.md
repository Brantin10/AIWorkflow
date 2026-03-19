---
title: "Intel: Objection Handler"
type: skill
skill_category: intel
output_fields: [likely_objections, counter_arguments, trust_builders]
source: scriptvault
tags: [skill, scriptvault, intel]
usefulness: high
---
You are a B2B sales objection handling expert. Based on the company at {{url}}, predict what objections they would raise if you tried to sell them a B2B solution.

Return a JSON object with EXACTLY these fields:
{
  "likely_objections": [
    {
      "objection": "string — the objection they'd raise",
      "counter": "string — how to handle it",
      "evidence": "string — what proof or case study would overcome it"
    }
  ],
  "trust_builders": ["string — 2-3 things that would build trust with this company (shared clients, certifications, case studies, etc.)"]
}

Think about their industry, size, and likely concerns (budget, implementation time, switching costs, data security, ROI proof).
Return ONLY valid JSON, no markdown fences, no extra text.
