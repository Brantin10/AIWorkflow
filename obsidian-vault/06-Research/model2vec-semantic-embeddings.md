---
title: "Model2Vec Static Embeddings for Semantic Search"
created: "2026-03-18"
updated: "2026-03-18"
tags: [research, embeddings, nlp, semantic-search, ml, ai]
status: active
type: research
usefulness: high
read-count: 0
source-project: JARVIS
---

# Model2Vec Static Embeddings for Semantic Search

## Overview
Model2Vec provides lightweight static word embeddings that can be used for semantic similarity search without GPU inference. JARVIS uses the `potion-base-8M` model for memory search.

## Key Specs
- **Model:** `minishlab/potion-base-8M`
- **Dimensions:** 256
- **Size:** ~8MB (compared to 400MB+ for sentence-transformers)
- **Speed:** Single encode in <1ms, batch of 200 in ~50ms
- **No GPU required**

## Usage

```python
from model2vec import StaticModel
import numpy as np

# Load model (cached after first download)
model = StaticModel.from_pretrained("minishlab/potion-base-8M")

# Single encode
embedding = model.encode(["What is the CPU temperature?"])[0]  # shape: (256,)

# Batch encode (much faster for backfill)
embeddings = model.encode(["query 1", "query 2", "query 3"])  # shape: (3, 256)

# Cosine similarity
def cosine_sim(a, b):
    a_norm = a / (np.linalg.norm(a) + 1e-10)
    b_norm = b / (np.linalg.norm(b) + 1e-10)
    return float(np.dot(a_norm, b_norm))
```

## Storage in SQLite
```python
# Store as BLOB
blob = embedding.astype(np.float32).tobytes()  # 256 * 4 = 1024 bytes
cursor.execute("INSERT INTO embeddings (id, embedding) VALUES (?, ?)", (id, blob))

# Retrieve
emb = np.frombuffer(row["embedding"], dtype=np.float32)  # shape: (256,)
```

## Comparison with Alternatives
| Model | Dims | Size | Speed | Quality |
|-------|------|------|-------|---------|
| potion-base-8M | 256 | 8MB | <1ms | Good |
| all-MiniLM-L6-v2 | 384 | 80MB | ~10ms | Better |
| BGE-base-en | 768 | 440MB | ~30ms | Best |

## Key Findings
- Sufficient quality for conversation memory search (0.3 cosine threshold works well)
- Not suitable for production RAG systems (use sentence-transformers instead)
- Background loading avoids blocking startup (~2s to load model)
- Batch backfill of 50K conversations takes ~4 minutes
