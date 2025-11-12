from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from dependencies.auth import get_current_user
from firestore import upload_user_image_to_firebase, delete_photo_from_firebase
from models import usersModel
from schemes.userSchemes import UserResponse, UserCreate, UserUpdate
from utils.email import generate_verification_code, send_verification_email
from utils.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#CREAR USUARIO
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    existing_user = db.query(usersModel.Users).filter(usersModel.Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    verification_code = generate_verification_code()
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=10)

    db_user = usersModel.Users(
        **user.model_dump(exclude={"password"}),
        password=hashed_pw,
        verification_code=verification_code,
        verification_expiration=expiration_time,
        is_verified=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    background_tasks.add_task(send_verification_email, user.email, verification_code)

    return db_user

#SUBIR FOTO
@router.post("/upload-photo")
async def upload_photo(
        photo: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: usersModel.Users = Depends(get_current_user)
):
    contents = await photo.read()
    public_url = upload_user_image_to_firebase(contents, photo.filename)

    current_user.photo = public_url
    db.commit()
    db.refresh(current_user)

    return {
        "message": "Updated profile photo",
        "url": public_url
    }

#ACTUALIZAR FOTO
@router.put("/update-photo")
async def update_photo(
        photo: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: usersModel.Users = Depends(get_current_user)
) :
    if current_user.photo:
        delete_photo_from_firebase(current_user.photo)

    contents = await photo.read()
    public_url = upload_user_image_to_firebase(contents, photo.filename)

    current_user.photo = public_url
    db.commit()
    db.refresh(current_user)
    return {
        "message": "Updated profile photo",
    }

#BORRAR FOTO
@router.delete("/delete-photo")
def delete_photo(
        current_user: usersModel.Users = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if current_user.photo:
        delete_photo_from_firebase(current_user.photo)
        current_user.photo = None
        db.commit()
        db.refresh(current_user)
        return {
            "message": "Deleted profile photo",
        }
    raise HTTPException(status_code=404, detail="Photo not found")

#OBTENER TODOS LOS USUARIOS
@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: usersModel.Users = Depends(get_current_user)):
    return db.query(usersModel.Users).all()

#OBTENER USUARIO POR ID
@router.get("/id", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(usersModel.Users).filter(usersModel.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

#OBTENER USUARIO POR EMAIL
@router.get("/email", response_model=UserResponse)
def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
    user = db.query(usersModel.Users).filter(usersModel.Users.email == user_email).first()
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