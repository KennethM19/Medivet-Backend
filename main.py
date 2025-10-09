from fastapi import FastAPI

from database import engine, Base
from routers import users

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Medivet Backend")

app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "Hello World"}