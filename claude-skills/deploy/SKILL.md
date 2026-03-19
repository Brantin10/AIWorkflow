---
name: deploy
description: Build and deploy the project to Vercel production. Use when asked to deploy, push to production, go live, ship it, or sync the website.
disable-model-invocation: true
argument-hint: "[project-name]"
---

# Deploy to Vercel

Deploy the current project to Vercel production.

## Prerequisites

Before running, ensure Node.js is in PATH. On Windows sandbox:
```
export PATH="/c/Program Files/nodejs:$PATH"
```

## Steps

1. **Build** — Run `npm run build`. If it fails, fix the errors and retry.
2. **Deploy** — Run `npx vercel --prod --yes`
3. **Verify alias** — Check the output for the aliased URL. If the alias doesn't match the expected domain, run `npx vercel alias set <deployment-url> <expected-domain>`
4. **Verify live** — Fetch the production URL and confirm it returns status 200.

## Output

Report exactly:
- Build: PASS / FAIL
- Deploy URL: [url]
- Alias: [url]
- Status: LIVE / FAILED

If any step fails, report the error and stop.

## Rules

- Never skip the build step
- Never deploy if the build fails
- Always verify the alias after deployment
- If `--prod --yes` creates a new project, warn the user immediately
