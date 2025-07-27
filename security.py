# backend/security.py
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import HTTPException, status
from config import settings

def authenticate_admin(email: str, password: str):
    
    if email == settings.ADMIN_EMAIL and password == settings.ADMIN_PASSWORD:
        return {
            "email": email,
            "is_admin": True
        }
    return False

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Создаем JWT токен"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Проверяем токен"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return {"email": email, "is_admin": True}
    except JWTError as e:
        return None