---
name: fix-mobile
description: >
  Fixes mobile responsiveness issues. Use when something looks broken on phone,
  doesn't fit on mobile, is overflowing, cut off, too wide, unsynced on small screens,
  or needs responsive design fixes.
argument-hint: "[file-or-component]"
allowed-tools: Read, Grep, Glob
---

# Fix Mobile Responsiveness

Fix mobile layout issues in `$ARGUMENTS`.

## Diagnosis Steps

1. Read the component and its CSS/Tailwind classes
2. Identify fixed pixel widths that exceed 375px (standard phone width)
3. Check for `overflow-hidden` on parent containers that may clip content
4. Look for flex/grid layouts that don't wrap or stack on small screens
5. Check for elements with fixed positioning that break on mobile

## Common Fixes

| Problem | Solution |
|---------|----------|
| Two items side by side too wide | Stack vertically on small screens: `flex-col sm:flex-row` |
| Fixed width too large | Use responsive: `w-full max-w-[250px]` or smaller mobile sizes |
| Content clipped | Change `overflow-hidden` to `overflow-x-clip` or `overflow-visible` |
| Text too large | Add responsive sizes: `text-2xl sm:text-3xl lg:text-5xl` |
| Padding/gap too big | Reduce on mobile: `gap-2 sm:gap-4 lg:gap-8` |
| Element hidden/cut off | Use `hidden sm:block` to hide on smallest screens |

## Approach

1. Fix the smallest screen first (375px)
2. Then ensure it looks good at 640px (sm), 768px (md), 1024px (lg)
3. Never break the desktop layout while fixing mobile

## Output

After fixing:
- List each change made
- State what screen sizes were affected
- Confirm desktop layout is unchanged

## Rules

- Always check parent containers for overflow clipping
- Prefer Tailwind responsive prefixes over CSS media queries
- Prefer stacking (flex-col) over scaling (transform: scale)
- Test that the fix doesn't break tablet or desktop views
- Don't add horizontal scrolling as a solution
