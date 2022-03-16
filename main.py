from fastapi import FastAPI, Request
from routers import admin
import models
import uvicorn
from database import engine
from fastapi.middleware.cors import CORSMiddleware
import os,glob

app = FastAPI()
app.include_router(admin.router)
models.Base.metadata.create_all(bind=engine)


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return os.listdir()
@app.get('/1')
def home():
    return os.path.abspath("")



if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")