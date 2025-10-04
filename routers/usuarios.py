from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=schemas.UserResponse)
def crear_usuario(usuario: schemas.UserCreate, db: Session = Depends(get_db)):
    db_usuario = models.User(nombre=usuario.nombre, correo=usuario.correo, contrasena=usuario.contrasena)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario