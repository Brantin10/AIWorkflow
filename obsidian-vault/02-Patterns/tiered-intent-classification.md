---
title: "Tiered Intent Classification"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, python, ml, nlp, classification]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: JARVIS
---

# Tiered Intent Classification

## Problem
Voice assistants need to route inputs to either "chat" (conversational) or "command" (tool-calling) paths. Regex alone is fragile; ML alone is slow for obvious cases.

## Solution
Three-tier cascade where each tier only fires if the previous one was not confident enough:

1. **Tier 1: Regex fast-path** (~0ms) — Catches obvious greetings and tool keywords
2. **Tier 2: TF-IDF + Logistic Regression** (~0.05ms) — Handles ambiguous cases with bag-of-words
3. **Tier 3: Model2Vec + Logistic Regression** (~0.4ms) — Semantic fallback for hard cases

## Code

```python
class IntentClassifier:
    def classify(self, text: str) -> tuple[str, float]:
        # Tier 1: Regex
        has_tool_kw = bool(_TOOL_KEYWORDS.search(text))
        has_chat = bool(_CHAT_OPENERS.search(text))
        if has_tool_kw and not has_chat:
            return ("command", 0.95)
        if has_chat and not has_tool_kw:
            return ("chat", 0.95)

        # Tier 2: TF-IDF (if loaded)
        if self._tfidf_pipeline:
            proba = self._tfidf_pipeline.predict_proba([text])[0]
            if max(proba) > 0.70:
                return (label, max(proba))

        # Tier 3: Model2Vec semantic
        if self._m2v_model:
            embedding = self._m2v_model.encode([text])
            proba = self._m2v_classifier.predict_proba(embedding)[0]
            return (label, max(proba))

        # Fallback: default to command (safety-first)
        return ("command", 0.5)
```

## Key Points
- Total added latency: <0.5ms — negligible vs LLM inference (1-15s)
- Regex tier handles ~70% of inputs, ML tiers handle the rest
- Train offline with `train_classifier.py`, load pickled models at startup
- Fallback defaults to "command" (safety-first: better to try tools than miss a command)
