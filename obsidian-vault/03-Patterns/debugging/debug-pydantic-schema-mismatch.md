---
title: "Debug: Pydantic schema field name mismatches (422 errors)"
type: debug-playbook
category: "api"
stack: "Python + React"
date: "2026-03-18"
tags:
  - debug
  - pattern
  - stack/python
  - stack/fastapi
---
# Debug: Pydantic Schema Field Name Mismatches

## Symptoms
- API returns 422 Validation Error on POST/PUT requests
- Frontend forms submit successfully but backend rejects the data
- Error messages mention "field required" for fields that ARE being sent

## Root Cause
Frontend field names don't match backend Pydantic schema field names. Common mismatches:
- `institution` vs `school`
- `field_of_study` vs `field`
- `start_date` vs `start_year`
- `url` vs `link`
- `technologies` as string vs `list[str]`

## Fix
1. Read the Pydantic schema in `schemas/*.py` — this is the source of truth
2. Update frontend form field names to match exactly
3. Check data types (string vs list, int vs string)
4. Test with `curl` directly to isolate frontend vs backend issue

## Prevention
- Always read the schema before building forms
- Use TypeScript types generated from Pydantic schemas (or shared type definitions)
- Test API endpoints with curl/httpx before building UI
