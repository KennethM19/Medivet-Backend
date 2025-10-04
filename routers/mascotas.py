from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter(prefix="/mascotas", tags=["Mascotas"])

@router.post("/", response_model=schemas.PetResponse)
def crear_mascota(mascota: schemas.PetCreate, db: Session = Depends(get_db)):
    # Verificar que exista el usuario
    usuario = db.query(models.User).filter(models.User.id == mascota.dueño_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db_mascota = models.Pet(
        nombre=mascota.nombre,
        especie=mascota.especie,
        dueño_id=mascota.dueño_id
    )
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota