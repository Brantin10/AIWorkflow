---
title: "Multi-Skill .md Pipeline Pattern"
created: "2026-03-19"
updated: "2026-03-19"
tags: [pattern, skills, pipeline, vault, intel, prompts]
status: active
type: pattern
usefulness: high
read-count: 0
---

# Multi-Skill .md Pipeline Pattern

Load `.md` files from the Obsidian vault as AI prompt templates, run each as a separate conversation, and merge results. Adding new skills requires zero code changes — just drop a new `.md` file.

## How It Works

```
Vault Folder (e.g., 07-Skills/)
  ├── intel-company-overview.md
  ├── intel-tech-stack.md
  ├── intel-pain-points.md
  └── intel-competitors.md
          │
          ▼
   Scan & Parse Each File
   (frontmatter + prompt body)
          │
          ▼
   Replace {{variables}} in prompt
          │
          ▼
   Run each skill as separate ChatGPT conversation
   (new_conversation between each)
          │
          ▼
   Merge all results into single report
```

## Skill File Format

Each `.md` skill file has YAML frontmatter and a prompt body:

```markdown
---
title: "Company Overview Intel"
skill_category: intel
output_fields: [company_name, industry, size, founded, hq, description]
model: chatgpt
---

You are a B2B sales researcher. Analyze the following company and provide a structured overview.

Company URL: {{url}}

Return your analysis as JSON with these fields:
- company_name: string
- industry: string
- size: string (employee range)
- founded: number (year)
- hq: string (city, country)
- description: string (2-3 sentences)
```

## Implementation

### 1. Scan Vault Folder for Skill Files

```python
from pathlib import Path
import yaml

VAULT_SKILLS_DIR = Path("C:/Users/oliver/Obsidian/DevVault/07-Skills")

def discover_skills(prefix: str = "intel-") -> list[dict]:
    """Find all skill .md files matching prefix."""
    skills = []
    for md_file in VAULT_SKILLS_DIR.glob(f"{prefix}*.md"):
        content = md_file.read_text(encoding="utf-8")
        skill = parse_skill_file(content)
        skill["filename"] = md_file.name
        skills.append(skill)
    return skills
```

### 2. Parse YAML Frontmatter + Prompt Body

```python
def parse_skill_file(content: str) -> dict:
    """Extract frontmatter and prompt from a skill .md file."""
    if not content.startswith("---"):
        return {"frontmatter": {}, "prompt": content}

    # Find closing ---
    end = content.index("---", 3)
    frontmatter_str = content[3:end].strip()
    prompt = content[end + 3:].strip()

    frontmatter = yaml.safe_load(frontmatter_str)
    return {
        "frontmatter": frontmatter,
        "prompt": prompt,
        "title": frontmatter.get("title", "Unknown Skill"),
        "output_fields": frontmatter.get("output_fields", []),
        "model": frontmatter.get("model", "chatgpt"),
        "category": frontmatter.get("skill_category", "general"),
    }
```

### 3. Replace Variables in Prompt

```python
def fill_variables(prompt: str, variables: dict) -> str:
    """Replace {{key}} placeholders with values."""
    for key, value in variables.items():
        prompt = prompt.replace(f"{{{{{key}}}}}", str(value))
    return prompt
```

### 4. Run Each Skill as Separate Conversation

```python
async def run_skill_pipeline(
    skills: list[dict],
    variables: dict
) -> dict:
    """Run all skills and merge results."""
    results = {}

    for skill in skills:
        await new_conversation()  # Clean context per skill
        filled_prompt = fill_variables(skill["prompt"], variables)

        try:
            raw = await call_proxima(filled_prompt, model=skill["model"])
            parsed = parse_json_response(raw)
            results[skill["category"]] = {
                "title": skill["title"],
                "data": parsed,
                "status": "success"
            }
        except Exception as e:
            logger.warning(f"Skill {skill['title']} failed: {e}")
            results[skill["category"]] = {
                "title": skill["title"],
                "data": None,
                "status": "error",
                "error": str(e)
            }

    return results
```

## Adding a New Skill

1. Create a new `.md` file in the skills folder, e.g., `intel-funding-history.md`
2. Add YAML frontmatter with `title`, `skill_category`, `output_fields`
3. Write the prompt body with `{{variable}}` placeholders
4. Done. No code changes. The pipeline discovers it on next run.

## Key Design Decisions

- **Separate conversations per skill**: Prevents context contamination between different research angles
- **YAML frontmatter**: Makes skills machine-queryable (filter by category, know expected output fields)
- **Variable replacement**: Same skill works for any target by swapping `{{url}}`, `{{company}}`, etc.
- **Graceful failure**: One skill failing doesn't kill the pipeline; results note which skills succeeded/failed

## Real-World Usage in ScriptVault

The intel pipeline uses this pattern to research prospects:
1. `intel-company-overview.md` — Basic company info
2. `intel-tech-stack.md` — Technology stack analysis
3. `intel-pain-points.md` — Industry pain points
4. `intel-competitors.md` — Competitive landscape
5. `intel-buying-signals.md` — Recent buying signals

All results merge into a single intel report that feeds the script generation engine.
