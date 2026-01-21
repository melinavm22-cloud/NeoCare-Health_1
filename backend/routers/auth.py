from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from backend.core.config import (
    get_db,
    SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    BCRYPT_ROUNDS
)
from backend.models.user import User
from backend.models.board import Board
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr, constr
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from backend.core.logging_config import log_auth_attempt
import logging

logger = logging.getLogger("neocare.auth")

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer()

# --- Schemas ---
class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=8, max_length=100)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)

# --- Registro ---
@router.post("/register")
def register(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        logger.warning(f"Intento de registro con email duplicado: {user.email}")
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed_pw = pwd_context.hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    default_board = Board(title="Mi primer tablero", user_id=new_user.id)
    db.add(default_board)
    db.commit()
    db.refresh(default_board)

    logger.info(f"Nuevo usuario registrado: {user.email} (ID: {new_user.id})")
    return {"msg": "Usuario registrado", "id": new_user.id, "default_board_id": default_board.id}

# --- Login ---
@router.post("/login", response_model=TokenResponse)
def login(login_request: LoginRequest, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "unknown"
    
    user = db.query(User).filter(User.email == login_request.email).first()
    if not user or not pwd_context.verify(login_request.password, user.password_hash):
        log_auth_attempt(login_request.email, False, client_ip)
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token_data = {
        "sub": user.email,
        "user_id": user.id,
        "username": user.username
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token({"sub": user.email, "user_id": user.id})
    
    log_auth_attempt(login_request.email, True, client_ip)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# --- Refresh Token ---
@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Token type inválido")
        
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if not email or not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
        token_data = {
            "sub": user.email,
            "user_id": user.id,
            "username": user.username
        }
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token({"sub": user.email, "user_id": user.id})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

# --- Dependencia centralizada para autenticación ---
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token type inválido")
        
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if not email or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    return user

@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"msg": "Logout exitoso"}



