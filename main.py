from fastapi import FastAPI
from routers import admin, authentication
import models
import uvicorn
from database import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(admin.router)
app.include_router(authentication.router)

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {'details': 'This is home page '}


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
