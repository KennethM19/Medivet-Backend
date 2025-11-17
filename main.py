from fastapi import FastAPI

from database import engine, Base
from routers import usersRouter, authRouter, utilsRouter, petsRouter, medicalRecordRouter, chatRouter

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Medivet Backend")

app.include_router(authRouter.router)
app.include_router(usersRouter.router)
app.include_router(petsRouter.router)
app.include_router(utilsRouter.router)
app.include_router(medicalRecordRouter.router)
app.include_router(chatRouter.router)

@app.get("/")
def home():
    return {"message": "Hello World"}