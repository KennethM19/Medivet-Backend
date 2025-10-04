from fastapi import APIRouter
from firestore import db_firestore
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/predicciones", tags=["Predicciones"])

class Predicciones(BaseModel):
    mascota_id: int
    resultado: str
    probabilidad: float

@router.get("/")
def guardar_prediccion(pred: Predicciones):
    data = {
        "mascota_id": pred.mascota_id,
        "resultado": pred.resultado,
        "probabilidad": pred.probabilidad,
        "fecha": datetime.now().isoformat()
    }

    db_firestore.collection("Mascotas").document(str(pred.mascota_id))\
        .collection("Predicciones_NLP").add(data)

    return {"mensaje": "Predicción guardada en Firestore", "data": data}