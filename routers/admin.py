from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from repository import admin
from database import get_db
import schemas
from routers import oauth2
router = APIRouter(tags=['admin'], prefix='/admin')


@router.post('/uploadcsv', status_code=status.HTTP_201_CREATED)
async def upload_csv(name_in_which_col: int = Form(...), email_in_which_col: int = Form(...), css: UploadFile = File(...), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return admin.upload_csv(int(name_in_which_col), int(email_in_which_col), css)


@router.post('/stage1', status_code=status.HTTP_201_CREATED)
async def stage1(request: schemas.Upload, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return admin.stage1(db, request)


@router.post('/stage2', status_code=status.HTTP_201_CREATED)
async def stage2(select: int = Form(...), db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return admin.stage2(select, db)


@router.get('/show_all')
def show_all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return admin.show_all(db)


@router.get('/find')
async def find(select: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return admin.find(select, db)


@router.get('/download')
def download(current_user: schemas.User = Depends(oauth2.get_current_user)):
    return FileResponse(admin.download(), media_type="application/pdf", filename='download.pdf')


@router.delete('/delete')
def delete(select: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return admin.delete(select, db)


@router.put('/update')
def update(select: int, name: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return admin.update(select, name, db)


