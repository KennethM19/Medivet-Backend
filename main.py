from fastapi import FastAPI

from database import engine, Base
from routers import usersRouter, authRouter, rolesRouter

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Medivet Backend")

app.include_router(authRouter.router)
app.include_router(usersRouter.router)
app.include_router(rolesRouter.router)

@app.get("/")
def home():
    return {"message": "Hello World"}