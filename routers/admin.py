from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from repository import admin
from database import get_db
import schemas

router = APIRouter(tags=['admin'], prefix='/admin')


@router.post('/uploadcsv', status_code=status.HTTP_201_CREATED)
async def upload_csv(name_in_which_col: int = Form(...), email_in_which_col: int = Form(...), css: UploadFile = File(...)):
    return admin.upload_csv(int(name_in_which_col), int(email_in_which_col), css)


@router.post('/stage1', status_code=status.HTTP_201_CREATED)
async def stage1(request: schemas.Upload, db: Session = Depends(get_db)):
    return admin.stage1(db, request)


@router.get('/stage2', status_code=status.HTTP_201_CREATED)
async def stage2(select: int, db: Session = Depends(get_db)):
    return admin.stage2(select, db)


@router.get('/show_all')
def show_all(db: Session = Depends(get_db)):
    return admin.show_all(db)


@router.get('/download')
async def download():
    return FileResponse(admin.download())


@router.get('/download_pdf')
async def download():
    return FileResponse(admin.show())