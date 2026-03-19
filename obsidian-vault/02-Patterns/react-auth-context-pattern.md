---
title: "React Auth Context Pattern"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, react, javascript, auth, context]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: AIResume
---

# React Auth Context Pattern

## Problem
Need global auth state (user, token, loading) accessible across all components, with automatic token validation on mount and clean logout.

## Solution
React Context with `useCallback`/`useMemo` optimized login/register/logout functions. Token stored in localStorage, validated on mount by calling the `/auth/me` endpoint.

## Code

```jsx
import { createContext, useState, useEffect, useCallback, useMemo } from 'react';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  // Validate token on mount
  useEffect(() => {
    let cancelled = false;
    async function loadUser() {
      const storedToken = localStorage.getItem('token');
      if (!storedToken) { setLoading(false); return; }
      try {
        const userData = await getCurrentUser(); // GET /auth/me
        if (!cancelled) { setUser(userData); setToken(storedToken); }
      } catch {
        localStorage.removeItem('token');
        if (!cancelled) { setUser(null); setToken(null); }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    loadUser();
    return () => { cancelled = true; };
  }, []);

  const login = useCallback(async (email, password) => {
    const data = await loginUser(email, password);
    const newToken = data.access_token;
    localStorage.setItem('token', newToken);
    setToken(newToken);
    const userData = await getCurrentUser();
    setUser(userData);
    return userData;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setToken(null);
  }, []);

  const value = useMemo(() => ({
    user, token, loading, login, logout,
    isAuthenticated: !!token && !!user,
  }), [user, token, loading, login, logout]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
```

## Key Points
- `cancelled` flag prevents state updates on unmounted component
- Token validated on mount — catches expired tokens immediately
- `useMemo` on context value prevents unnecessary re-renders
- `useCallback` on login/logout prevents child re-renders
- After login, always fetch fresh user data (don't trust the login response alone)
