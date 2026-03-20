#!/bin/bash
# =============================================================
# Claude Code Config Installer — Run on Mac to sync setup
# =============================================================
# This script copies hooks, CLAUDE.md, and settings from the
# Obsidian vault sync to ~/.claude/ on your Mac.
#
# Usage:
#   cd ~/Obsidian/DevVault/01-Projects/claude-code-config
#   chmod +x setup-mac.sh
#   ./setup-mac.sh
# =============================================================

set -e

CLAUDE_DIR="$HOME/.claude"
HOOKS_DIR="$CLAUDE_DIR/hooks"
VAULT_PATH="$HOME/Obsidian/DevVault"  # Adjust if different on Mac

echo "=== Claude Code Config Installer ==="
echo ""

# Create directories
mkdir -p "$HOOKS_DIR"
echo "✓ Created $HOOKS_DIR"

# Copy hooks (fix vault path for Mac)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

for f in on-session-start.py on-stop.py on-edit.py orchestrator_client.py; do
    if [ -f "$SCRIPT_DIR/$f" ]; then
        # Copy and fix Windows paths to Mac paths
        sed \
            -e "s|C:\\\\Users\\\\oliver\\\\Obsidian\\\\DevVault|$VAULT_PATH|g" \
            -e "s|C:/Users/oliver/Obsidian/DevVault|$VAULT_PATH|g" \
            -e 's|C:\\\\Users\\\\oliver\\\\Desktop\\\\|~/Desktop/|g' \
            -e 's|C:/Users/oliver/Desktop/|~/Desktop/|g' \
            -e 's|C:\\\\Users\\\\oliver\\\\|~/|g' \
            -e 's|C:/Users/oliver/|~/|g' \
            "$SCRIPT_DIR/$f" > "$HOOKS_DIR/$f"
        chmod +x "$HOOKS_DIR/$f"
        echo "✓ Installed $f"
    fi
done

# Copy CLAUDE.md
if [ -f "$SCRIPT_DIR/CLAUDE.md" ]; then
    cp "$SCRIPT_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
    echo "✓ Installed CLAUDE.md"
fi

# Copy settings.json (fix python path for Mac)
if [ -f "$SCRIPT_DIR/settings.json" ]; then
    # Replace Windows python path with Mac python3
    sed \
        -e 's|C:/Python314/python.exe|python3|g' \
        -e 's|C:/Users/oliver/.claude/hooks/|'"$HOOKS_DIR"'/|g' \
        "$SCRIPT_DIR/settings.json" > "$CLAUDE_DIR/settings.json"
    echo "✓ Installed settings.json (paths adjusted for Mac)"
fi

echo ""
echo "=== Done! ==="
echo "Restart Claude Code to pick up the new hooks."
echo ""
echo "Hooks installed:"
ls -la "$HOOKS_DIR"
echo ""
echo "CLAUDE.md:"
ls -la "$CLAUDE_DIR/CLAUDE.md"
