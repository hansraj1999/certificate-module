from fastapi import APIRouter, Depends, status, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from repository import admin
from database.database import get_db
import schemas
from routers import oauth2

router = APIRouter(tags=['admin'], prefix='/admin')


@router.post('/uploadcsv', status_code=status.HTTP_201_CREATED)
async def upload_csv(name_in_which_col: int = Form(...), email_in_which_col: int = Form(...), css: UploadFile = File(...), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return admin.upload_csv(int(name_in_which_col), int(email_in_which_col), css)


@router.post('/stage1', status_code=status.HTTP_201_CREATED)
async def insert_into_db(request: schemas.Upload, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return admin.insert_into_db(db, request)


@router.post('/stage2', status_code=status.HTTP_201_CREATED)
async def generate_certificate(select: int = Form(...), db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return admin.generate_certificate(select, db)


@router.get('/show_all')
def show_all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return admin.show_all(db)


@router.post('/find')
async def find(select: int = Form(...), db: Session = Depends(get_db)):
    return admin.find(select, db)


@router.get('/download')
def download(current_user: schemas.User = Depends(oauth2.get_current_user)):
    return FileResponse(admin.download(), media_type="application/pdf", filename='download.pdf')


@router.delete('/delete')
def delete(select: int = Form(...), db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return admin.delete(select, db)


@router.put('/update')
def update(select: int = Form(...), name: str = Form(...), db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return admin.update(select, name, db)


@router.get('/finds/{u_id}')
def finds(u_id, db: Session = Depends(get_db)):
    return admin.finds(u_id, db)


@router.get('/specific_download')
def specific_download(u_id: int, db: Session = Depends(get_db)):
    if admin.specific_download(u_id, db) == {'response': False}:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Certificate with {u_id} is not available")
    return FileResponse(admin.specific_download(u_id, db), media_type="application/pdf", filename='download.pdf')
