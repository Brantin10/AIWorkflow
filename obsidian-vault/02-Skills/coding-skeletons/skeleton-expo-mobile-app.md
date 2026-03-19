---
title: "Skeleton: Expo React Native Mobile App"
type: skeleton
stack: "React + Node.js"
category: "mobile"
tags:
  - skill
  - skill/skeleton
  - stack/react
  - stack/react-native
  - stack/expo
---
# Skeleton: Expo React Native Mobile App

## Use Case
Cross-platform mobile apps with file-based routing, Firebase backend, and rich animations. Used in [[01-Projects/myfuturecareer-rn]].

## File Structure
```
app/                     # Expo Router (file-based routing)
  _layout.tsx            # Root layout
  index.tsx              # Entry screen
  login.tsx, signup.tsx   # Auth screens
  onboarding.tsx         # Onboarding flow
  (tabs)/                # Tab navigation group
    home.tsx
    search.tsx
    profile.tsx
components/              # Reusable components
hooks/                   # Custom hooks
context/                 # Auth, app state
utils/                   # Helpers, API clients
assets/                  # Images, fonts
```

## Key Patterns
- **Expo Router**: File-based routing (like Next.js for mobile)
- **Firebase BaaS**: Auth + Firestore + Push notifications
- **AsyncStorage**: Persistent local preferences
- **Reanimated v4**: Performant, gesture-driven animations
- **Role-based UX**: Different navigation trees per user role

## Setup Commands
```bash
npx create-expo-app@latest --template tabs
npm install firebase @react-native-async-storage/async-storage
npm install react-native-reanimated react-native-gesture-handler
npx expo start
```
