---
title: "ADR: JSON Columns for Flexible Resume Schema"
created: "2026-03-18"
updated: "2026-03-18"
tags: [adr, architecture, database, sqlite, sqlalchemy]
status: active
type: adr
usefulness: high
read-count: 0
source-project: AIResume
---

# ADR: JSON Columns for Flexible Resume Schema

## Status
Accepted

## Context
Resumes have many optional sections (experience, education, skills, projects, certifications, languages, awards, links, custom sections). Each section has a different structure. Users can reorder sections.

Options:
1. **Normalized tables:** Separate table per section with foreign keys
2. **JSON columns:** Store each section as JSON text in a single Resume row
3. **Document store:** Use MongoDB or similar

## Decision
Store each section as a JSON-serialized TEXT column in a single `resumes` table:

```python
class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, default="Untitled Resume")
    template_name = Column(String, default="modern-pro")

    # JSON-serialised sections
    personal_info_json = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    experience_json = Column(Text, nullable=True)
    education_json = Column(Text, nullable=True)
    skills_json = Column(Text, nullable=True)
    projects_json = Column(Text, nullable=True)
    certifications_json = Column(Text, nullable=True)
    section_order_json = Column(Text, nullable=True)
    settings_json = Column(Text, nullable=True)
```

## Consequences
### Positive
- Single table, single query to load/save entire resume
- Adding new section types requires no migration
- Section order stored as JSON array — trivial to reorder
- SQLite handles it well (no need for PostgreSQL JSONB)

### Negative
- Cannot query individual section fields in SQL (no WHERE on skills)
- No referential integrity on section data
- Pydantic schemas must handle serialization/deserialization
- Section validation happens in application layer, not database

### Mitigations
- Pydantic models validate section structure on API input
- Full resume loaded/saved atomically — no partial updates needed
- If querying sections becomes necessary, can extract to separate tables later
