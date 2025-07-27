# backend/main.py
from datetime import timedelta
from fastapi import FastAPI, HTTPException, status, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import uvicorn
from config import settings
from security import authenticate_admin, create_access_token, verify_token
from routers import courses  # Добавляем импорт

app = FastAPI(title="Admin API", version="1.0.0")

# Расширенная CORS настройка
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://xn----7sbnsddslml5i.xn--p1ai",  # ваш домен
        "https://красный-код.рф",                 # ваш домен (если работает)
        "http://localhost:5173",                 # для локальной разработки
        "http://127.0.0.1:5173"                  # для локальной разработки
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(courses.router, prefix="/api/courses")

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    email: str
    is_admin: bool

class TokenData(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

@app.post("/api/auth/login", response_model=TokenData)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Вход в админку"""
    # Проверяем grant_type
    if form_data.grant_type and form_data.grant_type != "password":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Grant type must be password",
        )
    
    user = authenticate_admin(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    return TokenData(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(email=user["email"], is_admin=user["is_admin"])
    )

@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_admin(authorization: Optional[str] = Header(None)):
    """Получение информации о текущем админе"""
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Разделяем заголовок на части
        parts = authorization.split()
        if len(parts) != 2:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        scheme, token = parts
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return UserResponse(email=user["email"], is_admin=user["is_admin"])

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Admin Auth API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)