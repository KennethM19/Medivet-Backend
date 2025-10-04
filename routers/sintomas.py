from fastapi import APIRouter
from firestore import db_firestore
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/sintomas", tags=["Síntomas"])

class Sintomas(BaseModel):
    mascota_id: int
    desripcion: str

@router.post("/")
def reportar_sintomas(sintomas: Sintomas):
    data = {
        "mascota_id": sintomas.mascota_id,
        "desripcion": sintomas.desripcion,
        "fecha": datetime.now().isoformat(),
    }

    db_firestore.collection("Mascotas").document(str(sintomas.mascota_id))\
    .collection("Sintomas_Reportados").add(data)

    return {"mensaje": "Síntoma registrado en Firestore", "data": data}