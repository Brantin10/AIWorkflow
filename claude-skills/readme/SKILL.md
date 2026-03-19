---
name: readme
description: >
  Generates a README.md for the project. Use when asked to create documentation,
  write a readme, document the project, or create a README file.
argument-hint: "[directory]"
allowed-tools: Read, Grep, Glob
---

# Generate README

Generate a README.md for the project at `$ARGUMENTS` (default: current directory).

## Steps

1. Read package.json / Cargo.toml / pyproject.toml to identify project name, description, dependencies
2. Scan directory structure to understand architecture
3. Read key entry files to understand the purpose
4. Check for existing scripts (build, test, dev, deploy)

## README Structure

Output exactly this structure. Do not add or remove sections.

```markdown
# Project Name

One sentence description.

## Features

- Bullet list of 3-6 key features

## Tech Stack

- List each technology with brief purpose

## Getting Started

### Prerequisites

- What needs to be installed (Node.js version, etc.)

### Installation

Step-by-step commands to install and run locally.

### Build

Command to build for production.

## Project Structure

Brief directory tree with one-line descriptions for key folders.

## Deployment

How to deploy (if detectable from config).

## License

License type (if found in package.json or LICENSE file).
```

## Rules

- Keep it factual — only include what you can verify from the code
- Do not add badges or shields
- Do not add Contributing or Code of Conduct sections unless they already exist
- Do not add placeholder text like "Add description here"
- Commands must be copy-pasteable and correct
- If you can't determine something, omit it rather than guessing
