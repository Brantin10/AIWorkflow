# Mac Setup Prompt for Claude Code

Paste this into your first Claude Code session on the Mac to set everything up.

---

## Prompt:

```
I just cloned my AIWorkflow repo. Help me set up my Mac to match my Windows development environment. Here's what needs to happen:

1. **Claude Code Skills** — Copy skills to the right place:
   ```bash
   cp -r ~/Desktop/AIWorkflow/claude-skills/* ~/.claude/skills/
   ```

2. **Obsidian Vault** — Move to a permanent location:
   ```bash
   mkdir -p ~/Obsidian
   cp -r ~/Desktop/AIWorkflow/obsidian-vault ~/Obsidian/DevVault
   ```
   Then open Obsidian → Open folder as vault → ~/Obsidian/DevVault
   Enable Community Plugins when prompted.

3. **Claude Memory** — Copy project memories:
   ```bash
   for dir in ~/Desktop/AIWorkflow/claude-memory/*/; do
     name=$(basename "$dir")
     mkdir -p ~/.claude/projects/$name/memory
     cp -r "$dir"* ~/.claude/projects/$name/memory/
   done
   ```

4. **Environment variables** — Add to ~/.zshrc:
   ```bash
   echo 'export VAULT_PATH=~/Obsidian/DevVault' >> ~/.zshrc
   echo 'export SKILLS_DIR=~/Obsidian/DevVault/07-Skills' >> ~/.zshrc
   source ~/.zshrc
   ```

5. **Clone project repos** (only what you need):
   ```bash
   cd ~/Desktop
   git clone https://github.com/Brantin10/ScriptVault.git
   # git clone https://github.com/Brantin10/Orchestrator.git  # if needed
   ```

6. **Verify setup** — Run these checks:
   - `ls ~/.claude/skills/` should show 29 skill folders
   - `ls ~/Obsidian/DevVault/` should show 01-Projects through 09-ScriptVault
   - Start Claude Code in any project and try `/vault-read` or `/audit`

That's it. No heavy dependencies needed — just Git, Node.js, Python 3.11+, and Obsidian.
The vault is ~15MB of markdown files. Skills are ~500KB total.
```
