from fastapi import FastAPI
from routers import admin
import models
from database import engine

app = FastAPI()
app.include_router(admin.router)
models.Base.metadata.create_all(bind=engine)
