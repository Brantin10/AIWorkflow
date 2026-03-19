---
title: "Axios Interceptor Pattern"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, javascript, react, axios, http, error-handling]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: AIResume
---

# Axios Interceptor Pattern

## Problem
Every API call needs auth token injection, and error responses come in varied formats (FastAPI validation errors, generic errors, network errors). Need centralized handling.

## Solution
Axios instance with request interceptor for auth and response interceptor for error normalization + auto-logout on 401.

## Code

```javascript
import axios from 'axios';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
});

// Request: inject auth token
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Response: normalize errors
function extractErrorMessage(error) {
  if (!error.response) {
    if (error.code === 'ECONNABORTED') return 'Request timed out.';
    if (!navigator.onLine) return 'Network error.';
    return error.message;
  }
  const { data, status } = error.response;
  // FastAPI 422 validation errors
  if (status === 422 && Array.isArray(data?.detail)) {
    return data.detail.map(d => d.msg).join('. ');
  }
  if (typeof data?.detail === 'string') return data.detail;
  // Fallback by status code
  const fallbacks = { 400: 'Bad request.', 401: 'Session expired.', 500: 'Server error.' };
  return fallbacks[status] || `Request failed (${status}).`;
}

client.interceptors.response.use(
  (response) => response,
  (error) => {
    error.userMessage = extractErrorMessage(error);
    // Auto-logout on 401
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
```

## Usage in Components
```javascript
try {
  await client.post('/resumes', data);
} catch (error) {
  showToast(error.userMessage); // Always a human-readable string
}
```

## Key Points
- `error.userMessage` gives components a single string to display
- 401 auto-redirect prevents stale-token UX issues
- FastAPI 422 validation errors are flattened into readable messages
- Network errors and timeouts get user-friendly messages
