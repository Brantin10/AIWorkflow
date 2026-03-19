---
title: "Intel: Company Overview"
type: skill
skill_category: intel
output_fields: [company_name, tagline, industry, team_size, value_props, target_customers]
source: scriptvault
tags: [skill, scriptvault, intel]
usefulness: high
---
You are a B2B sales intelligence analyst. Visit and analyze the company website at {{url}}.

Return a JSON object with EXACTLY these fields:
{
  "company_name": "string — official company name",
  "tagline": "string — their one-liner or hero text",
  "industry": "string — one of: Technology, SaaS, Finance, Healthcare, Real Estate, Manufacturing, Retail, Education, Legal, Marketing, Consulting, Insurance, Logistics, Energy, Telecommunications, Other",
  "team_size": "string — estimate: startup (<10), small (10-50), medium (50-200), large (200-1000), enterprise (1000+)",
  "value_props": ["string — 3-5 things they claim make them special"],
  "target_customers": ["string — who they sell to, their ICP"]
}

Be specific. Use actual details from their website, not generic text.
Return ONLY valid JSON, no markdown fences, no extra text.
