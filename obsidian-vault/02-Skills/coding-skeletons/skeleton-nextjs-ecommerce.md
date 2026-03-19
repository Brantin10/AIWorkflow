---
title: "Skeleton: Next.js Ecommerce with Prisma"
type: skeleton
stack: "React + Node.js"
category: "fullstack"
tags:
  - skill
  - skill/skeleton
  - stack/react
  - stack/nextjs
  - stack/prisma
---
# Skeleton: Next.js Ecommerce with Prisma

## Use Case
Portfolio/shop sites with admin dashboard, auth, payments, and image storage. Used in [[01-Projects/artbyewelina]].

## File Structure
```
src/app/
  (public)/              # Public pages (home, shop, [slug], about, contact)
  admin/                 # Admin dashboard (artworks CRUD, orders)
  api/
    admin/artworks/      # CRUD API routes
    admin/orders/
  middleware.ts          # Auth/authorization checks
prisma/
  schema.prisma          # Data model
  seed.ts                # Initial data
```

## Key Patterns
- **Route groups**: `(public)` vs `admin` for layout separation
- **Prisma as truth**: Single schema, migrations, seeding
- **NextAuth v5**: Session management with Prisma adapter
- **Stripe**: Payment processing (checkout sessions)
- **Vercel Blob**: Scalable image storage with CDN

## Setup Commands
```bash
npx create-next-app@latest --ts --tailwind
npm install prisma @prisma/client next-auth@beta @auth/prisma-adapter stripe
npm install @vercel/blob zod zustand
npx prisma init && npx prisma db push
```
