from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from dependencies.auth import get_current_user
from models import usersModel
from schemes.userSchemes import UserResponse, UserCreate, UserUpdate
from utils.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#CREAR USUARIO
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(usersModel.Users).filter(usersModel.Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    db_user = usersModel.Users(**user.model_dump(exclude={"password"}), password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#OBTENER TODOS LOS USUARIOS
@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: usersModel.Users = Depends(get_current_user)):
    return db.query(usersModel.Users).all()

#OBTENER USUARIO POR ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: usersModel.Users = Depends(get_current_user)):
    user = db.query(usersModel.Users).filter(usersModel.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#ACTUALIZAR DATOS USUARIO
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_data: UserUpdate, db: Session = Depends(get_db), current_user: usersModel.Users = Depends(get_current_user)):
    user = db.query(usersModel.Users).filter(usersModel.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in updated_data.model_dump(exclude_unset=True).items():
        if key == "password" and value:
            value = hash_password(value)
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

#BORRAR USUARIO
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: usersModel.Users = Depends(get_current_user)):
    user = db.query(usersModel.Users).filter(usersModel.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()