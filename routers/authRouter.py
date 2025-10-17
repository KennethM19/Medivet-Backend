from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

import config
from database import get_db
from models import usersModel
from models.usersModel import VerifyRequest
from schemes.userSchemes import TokenResponse, LoginRequest
from utils.security import verify_password, create_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(usersModel.Users).filter(usersModel.Users.email == request.email).first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email no verified")

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/verify")
def verify_email(request: VerifyRequest, db: Session = Depends(get_db)):
    user = db.query(usersModel.Users).filter(usersModel.Users.email == request.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.is_verified:
        return {"mesage": "User already verified"}

    if user.verification_code != request.code:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect code")

    if user.verification_expiration < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Code expired")

    user.is_verified = True
    user.verification_code = None
    user.verification_expiration = None
    db.commit()
    return {"mesage": "User verified"}