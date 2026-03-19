---
title: "FastAPI JWT Auth Pattern"
created: "2026-03-18"
updated: "2026-03-18"
tags: [pattern, python, fastapi, auth, jwt]
status: active
type: pattern
usefulness: high
read-count: 0
source-project: AIResume
---

# FastAPI JWT Auth Pattern

## Problem
Need stateless authentication for a FastAPI + React SPA. Sessions are not ideal for API-first architectures.

## Solution
JWT tokens with bcrypt password hashing, HTTPBearer security scheme, and a `get_current_user` dependency.

## Code

### security.py
```python
from datetime import datetime, timedelta, timezone
import bcrypt
from jose import JWTError, jwt

ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
```

### deps.py — Current User Dependency
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

### Route usage
```python
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

## Key Points
- `HTTPBearer` auto-generates Swagger "Authorize" button
- Store email in JWT `sub` claim, not user ID (more readable in debugging)
- bcrypt handles salting automatically via `gensalt()`
- python-jose supports HS256 out of the box
- Register endpoint returns token immediately (auto-login after signup)
