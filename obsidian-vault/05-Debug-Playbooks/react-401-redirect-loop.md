---
title: "React 401 Redirect Loop Fix"
created: "2026-03-18"
updated: "2026-03-18"
tags: [playbook, react, auth, axios, debugging]
status: active
type: playbook
usefulness: high
read-count: 0
source-project: AIResume
---

# React 401 Redirect Loop Fix

## Symptom
After token expires, page redirects to /login endlessly, or the login page itself triggers 401 errors.

## Root Cause
Axios response interceptor redirects ALL 401s to /login, including the login request itself (which returns 401 on bad credentials).

## Fix
Check current path before redirecting:

```javascript
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      // Only redirect if NOT already on login page
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
```

## Additional Guards

### AuthContext: validate token on mount
```jsx
useEffect(() => {
  let cancelled = false;
  async function loadUser() {
    const token = localStorage.getItem('token');
    if (!token) { setLoading(false); return; }
    try {
      const user = await getCurrentUser();
      if (!cancelled) setUser(user);
    } catch {
      // Token invalid — clean up silently
      localStorage.removeItem('token');
      if (!cancelled) { setUser(null); setToken(null); }
    } finally {
      if (!cancelled) setLoading(false);
    }
  }
  loadUser();
  return () => { cancelled = true; };
}, []);
```

## Key Points
- Login endpoint 401 means bad credentials, not expired token — don't redirect
- Clean up localStorage before redirect to prevent stale token on next load
- `cancelled` flag prevents state updates after unmount (React strict mode double-mount)
