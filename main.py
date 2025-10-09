from fastapi import FastAPI

from database import engine, Base
from routers import users, auth

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Medivet Backend")

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "Hello World"}