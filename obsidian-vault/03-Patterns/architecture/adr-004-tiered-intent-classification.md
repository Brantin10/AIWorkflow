---
title: "ADR: Tiered intent classification (Regex > TF-IDF > Semantic)"
type: adr
status: accepted
project: "JARVIS"
date: "2026-03-18"
tags:
  - adr
  - pattern
  - stack/python
  - stack/ai
---
# ADR: Tiered Intent Classification

## Context
JARVIS needs to decide whether user input requires tool calling (command) or just conversation (chat). Sending everything to the LLM wastes time and tokens.

## Decision
Three-tier classification with fast fallback:
1. **Regex** (~0.01ms): Hardcoded patterns for obvious chat/command intent
2. **TF-IDF + Logistic Regression** (~0.05ms): Trained ML classifier
3. **Model2Vec Semantic** (~0.4ms): Embedding-based similarity for ambiguous cases

Plus **fast dispatch**: Regex routes that skip the LLM entirely for deterministic queries ("what time is it" → call `get_time()` directly).

## Consequences
- Total overhead: <0.5ms (vs 1-5s for LLM)
- Deterministic queries resolve in 0.05s instead of 3-15s
- Trade-off: Needs training data for TF-IDF model
- Fast dispatch bypasses LLM reasoning (less flexible)
