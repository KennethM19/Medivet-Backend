from fastapi import FastAPI
from database import Base, engine
from routers import sintomas, predicciones, usuarios, mascotas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Medivet Backend")

app.include_router(predicciones.router)
app.include_router(sintomas.router)
app.include_router(usuarios.router)
app.include_router(mascotas.router)

@app.get("/")
def root():
    return {"mensaje": "API funcionando 🚀"}