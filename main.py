from fastapi import FastAPI, Request, BackgroundTasks
from routers import admin,authentication
import models
import uvicorn
from database import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(admin.router)
app.include_router(authentication.router)

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "https://sskveky2pn.us-east-1.awsapprunner.com/",
    "https://sskveky2pn.us-east-1.awsapprunner.com/admin/uploadcsv",


]


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")