---
title: "Semantic Memory Search with Embeddings"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, python, embeddings, semantic-search, sqlite]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: JARVIS
---

# Semantic Memory Search with Embeddings

## Problem
Keyword search misses semantically similar content. Need to find past conversations about "CPU temperature" when searching for "system overheating."

## Solution
Store vector embeddings alongside conversation records. On search, compute query embedding and find nearest neighbors via cosine similarity.

## Code

```python
import numpy as np
from model2vec import StaticModel

class MemoryManager:
    def __init__(self):
        # Load embedding model in background thread
        self._embed_model = StaticModel.from_pretrained("minishlab/potion-base-8M")
        self._embed_dim = 256

    def save_message(self, content):
        cursor = self.conn.execute("INSERT INTO conversations ...", (content,))
        row_id = cursor.lastrowid
        # Compute and store embedding
        embedding = self._embed_model.encode([content])[0]
        blob = embedding.astype(np.float32).tobytes()
        self.conn.execute(
            "INSERT INTO embeddings (conversation_id, embedding) VALUES (?, ?)",
            (row_id, blob)
        )

    def semantic_search(self, query, top_k=5, min_score=0.3):
        query_emb = self._embed_model.encode([query])[0]
        query_norm = query_emb / (np.linalg.norm(query_emb) + 1e-10)

        rows = self.conn.execute(
            "SELECT e.embedding, c.content, c.timestamp "
            "FROM embeddings e JOIN conversations c ON e.conversation_id = c.id"
        ).fetchall()

        results = []
        for row in rows:
            emb = np.frombuffer(row["embedding"], dtype=np.float32)
            emb_norm = emb / (np.linalg.norm(emb) + 1e-10)
            score = float(np.dot(query_norm, emb_norm))
            if score >= min_score:
                results.append({"content": row["content"], "similarity": score})

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
```

## Backfill Existing Data
```python
def backfill_embeddings(self, batch_size=200):
    rows = self.conn.execute(
        "SELECT c.id, c.content FROM conversations c "
        "LEFT JOIN embeddings e ON c.id = e.conversation_id "
        "WHERE e.conversation_id IS NULL"
    ).fetchall()
    for batch in chunks(rows, batch_size):
        texts = [r["content"] for r in batch]
        embeddings = self._embed_model.encode(texts)  # batch encode
        for row, emb in zip(batch, embeddings):
            self._store_embedding(row["id"], emb)
```

## Key Points
- model2vec potion-base-8M: 256-dim, fast, no GPU needed
- Store embeddings as BLOB (np.float32.tobytes()) — compact and fast
- Batch encode for backfill performance
- Cosine similarity via dot product of normalized vectors
- Falls back to keyword search if embedding model not loaded
