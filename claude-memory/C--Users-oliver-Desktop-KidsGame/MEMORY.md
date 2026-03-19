# KidsGame Project Memory

## Environment
- Windows 11, npm at `C:\Program Files\nodejs\npm.cmd` (must use `powershell -Command "& 'C:\Program Files\nodejs\npm.cmd' ..."`)
- `npm`/`npx` not on bash PATH — always use powershell wrapper
- `.npmrc` has `legacy-peer-deps=true`

## Tech Stack
- Expo SDK 54, React 19, TypeScript 5.9, expo-router 6
- State: Zustand + persist (AsyncStorage)
- Animations: react-native-reanimated
- Path alias: `@/*` → `src/*`
- Theme: `useTheme()` from `src/theme/index.ts`

## Key Patterns
- All screens: `LinearGradient` → `SafeAreaView` → content
- Haptics: `triggerHaptic()` from `src/utils/haptics.ts`
- Sounds: `playSound()` from `src/utils/sounds.ts`
- GameDefinition includes `tier: 'free' | 'premium'`
- Purchase state in `src/stores/purchaseStore.ts` (RevenueCat)
- Parental gate (math question) guards settings + purchases
- 3 free games (color-score, i-spy, road-bingo), 5 premium

## Architecture
- `app/` = expo-router screens (file-based)
- `src/components/` = reusable UI
- `src/stores/` = Zustand stores
- `src/theme/` = colors, spacing, typography
- `src/constants/` = game registry, categories, instructions
- `src/types/` = TypeScript interfaces
- `src/utils/` = haptics, sounds, purchases
