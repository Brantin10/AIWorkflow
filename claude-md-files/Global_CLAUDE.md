# CLAUDE.md

## Workflow Orchestration

### 1. Plan Mode Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop
- After ANY correction from the user: update this file with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes -- don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests -- then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

---

## Task Management

1. **Plan First**: Write plan with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Show what changed and prove it works
6. **Capture Lessons**: Update lessons below after corrections

---

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Only touch what's necessary. No side effects with new bugs.
- **Ship It**: Don't over-discuss. Build, test, show results. Bias toward action.
- **Solo Builder**: Oliver builds alone. Use "I"/"my" not "we"/"our" in any user-facing copy or presentations.

---

## Oliver's Stack & Environment

### Hardware
- Windows 11, RTX 5070 Ti (16GB VRAM)
- CUDA 12.8, PyTorch 2.12

### Common Stack
- **Backend**: FastAPI + SQLAlchemy + Supabase (PostgreSQL)
- **Frontend**: React + TypeScript + Tailwind + shadcn/ui
- **AI**: ChatGPT via Proxima (localhost:3210), QLoRA fine-tuned Mistral-7B
- **Vault**: Obsidian DevVault for knowledge persistence
- **Presentations**: PptxGenJS (Node.js)

### Proxima (AI Gateway)
- URL: `http://localhost:3210/v1/chat/completions`
- Models: `chatgpt`, `perplexity`, `claude`, `gemini`
- Format: `{"model": "chatgpt", "messages": [{"role": "user", "content": "..."}]}`
- Response: `choices[0].message.content`
- Timeout: MINIMUM 120s, prefer 180s (Proxima can be slow: 30-90s per request)

---

## Lessons Learned

### Windows-Specific
- Use `node "C:\\path\\to\\file.js"` — don't `cd` to Windows paths in bash
- LibreOffice PDF conversion fails on Windows (AF_UNIX socket error) — use `python -m markitdown` instead
- File paths: always use forward slashes or escaped backslashes in commands
- EBUSY errors mean a file is open in another app — change output filename
- Python scripts that print to stdout need `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")` to avoid cp1252 encoding crashes
- Hook commands in settings.json must use full python path (`C:/Python314/python.exe`) and forward slashes — backslashes get mangled

### Git
- Always commit with descriptive messages
- Never amend — create new commits
- Don't push unless explicitly asked
- Never use -i (interactive) flags — not supported

### AI / LLM Integration
- Always strip markdown fences from AI responses (```json blocks)
- Always include the "CORE PHILOSOPHY" block in sales-related AI prompts
- Checkpoint long-running generation jobs — APIs can timeout mid-batch
- Don't assume DB is needed for standalone scripts — mock or skip gracefully

### Common Mistakes to Avoid
- Don't use "we/our" in user-facing copy — Oliver is a solo builder
- Don't write generic AI prompts — always include domain-specific philosophy
- Don't skip validation after changing scoring or ranking logic
- Don't poll background tasks in a tight loop — use wider intervals or notifications
