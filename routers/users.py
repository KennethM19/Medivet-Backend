from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

import config
import models
from database import get_db
from schemas import UserResponse, UserCreate, UserUpdate
from utils.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(models.Users).filter(models.Users.email == email).first()

    if user is None:
        raise credentials_exception

    return user

#CREAR USUARIO
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    db_user = models.Users(**user.dict(exclude={"password"}), password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#OBTENER TODOS LOS USUARIOS
@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    return db.query(models.Users).all()

#OBTENER USUARIO POR ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#ACTUALIZAR DATOS USUARIO
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_data: UserUpdate, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in updated_data.dict(exclude_unset=True).items():
        if key == "password" and value:
            value = hash_password(value)
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

#BORRAR USUARIO
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()