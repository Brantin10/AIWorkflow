---
title: "Proxima/ChatGPT Batch Processing Pattern"
created: "2026-03-19"
updated: "2026-03-19"
tags: [pattern, proxima, chatgpt, batch, api]
status: active
type: pattern
usefulness: high
read-count: 0
---

# Proxima/ChatGPT Batch Processing Pattern

How to batch-process items through ChatGPT or Perplexity via the Proxima MCP local API.

## Endpoint

```
POST http://localhost:3210/v1/chat/completions
```

## Request Format

```python
import httpx

async def call_proxima(prompt: str, model: str = "chatgpt") -> str:
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            "http://localhost:3210/v1/chat/completions",
            json={
                "model": model,  # "chatgpt" or "perplexity"
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )
        data = response.json()
        return data["choices"][0]["message"]["content"]
```

## Available Models
- `"chatgpt"` — Best for research, web analysis, broad knowledge tasks
- `"perplexity"` — Best for web search with citations, current events

## Batch Processing Rules

### 1. New Conversation Between Batches
Call `new_conversation` between batch groups to prevent context bleed:

```python
async def new_conversation():
    async with httpx.AsyncClient(timeout=30.0) as client:
        await client.post("http://localhost:3210/v1/new_conversation")
```

### 2. Batch Size: 5 Items Per Conversation
Processing more than 5 items in a single conversation degrades quality as context fills up. Reset after every 5.

```python
BATCH_SIZE = 5

for i in range(0, len(items), BATCH_SIZE):
    batch = items[i:i + BATCH_SIZE]
    await new_conversation()  # Clean context
    for item in batch:
        result = await call_proxima(build_prompt(item))
        results.append(result)
```

### 3. Timeout: 120 Seconds
ChatGPT responses through Proxima can be slow. Use 120s timeout minimum.

### 4. Fire-and-Forget Error Handling
Individual failures should not kill the batch. Log and continue:

```python
for item in batch:
    try:
        result = await call_proxima(build_prompt(item))
        results.append({"item": item, "result": result, "status": "success"})
    except Exception as e:
        logger.warning(f"Failed for {item}: {e}")
        results.append({"item": item, "result": None, "status": "error"})
```

## JSON Response Parsing

ChatGPT often wraps JSON in markdown code fences or returns malformed JSON. Use fallback parsing:

```python
import json
import re

def parse_json_response(text: str) -> dict:
    """Parse JSON from ChatGPT response with multiple fallbacks."""
    # Try 1: Direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try 2: Extract from code fences ```json ... ```
    match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Try 3: Find first { ... } or [ ... ] block
    for start_char, end_char in [('{', '}'), ('[', ']')]:
        start = text.find(start_char)
        if start != -1:
            depth = 0
            for i in range(start, len(text)):
                if text[i] == start_char:
                    depth += 1
                elif text[i] == end_char:
                    depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except json.JSONDecodeError:
                        break

    raise ValueError(f"Could not parse JSON from response: {text[:200]}")
```

## Complete Example: Intel Batch Processing

```python
async def run_intel_batch(prospects: list[dict]) -> list[dict]:
    results = []
    for i in range(0, len(prospects), 5):
        batch = prospects[i:i + 5]
        await new_conversation()

        for prospect in batch:
            prompt = f"Research {prospect['name']} at {prospect['company']}..."
            try:
                raw = await call_proxima(prompt)
                parsed = parse_json_response(raw)
                results.append({"prospect": prospect, "intel": parsed})
            except Exception as e:
                logger.warning(f"Intel failed for {prospect['name']}: {e}")
                results.append({"prospect": prospect, "intel": None})

    return results
```

## Gotchas
- Proxima must be running (Electron app on localhost:3210)
- `new_conversation` is critical — without it, later items get confused by earlier context
- ChatGPT sometimes returns partial JSON if the response is very long; keep prompts focused
- Rate limiting is handled by Proxima internally; no need for manual delays
