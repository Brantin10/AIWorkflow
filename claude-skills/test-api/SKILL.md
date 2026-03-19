---
name: test-api
description: >
  Creates test users and sends test requests to API endpoints. Use when asked to
  test an API, create test data, send a test request, try an endpoint, test the
  server, generate test payloads, or smoke test a service.
argument-hint: "[endpoint-or-url]"
allowed-tools: Read, Grep, Glob, Bash
---

# API Test Runner

Test the API endpoint or service at `$ARGUMENTS`.

## Steps

1. **Discover the API**
   - Read route files, schemas, and config to understand the expected request/response format
   - Identify required fields, optional fields, and field types
   - Find the base URL and port from config

2. **Build a realistic test payload**
   - Create a JSON payload that matches the schema exactly
   - Use realistic values (not "test123" or "foo") that exercise the full pipeline
   - Include all required fields and a mix of optional fields

3. **Send the request**
   - Use `curl` or `python requests` to POST/GET the endpoint
   - Set appropriate headers (Content-Type: application/json)
   - Use a generous timeout for ML/AI endpoints (up to 600s)

4. **Analyze the response**
   - Check HTTP status code
   - Validate response matches expected schema
   - Flag any errors, warnings, or unexpected values
   - Check for empty/null fields that should have data

## Output Format

```
ENDPOINT: [method] [url]
STATUS:   [code] [reason]
TIME:     [duration]

REQUEST PAYLOAD:
  [formatted JSON, truncated if large]

RESPONSE SUMMARY:
  [key fields and values from response]

ISSUES:
  - [any problems found, or "None"]

VERDICT: PASS / FAIL / PARTIAL
```

## Rules

- Never send real credentials, passwords, or payment info in test data
- If the server isn't running, say so clearly — don't retry endlessly
- For ML/AI endpoints, expect longer response times (2-10 min is normal)
- Save full response to a `test_result.json` file in the project root
- If an endpoint requires auth, flag it and ask the user
