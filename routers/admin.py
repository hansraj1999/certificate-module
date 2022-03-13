from fastapi import APIRouter, Depends, status, Response, HTTPException, UploadFile, File
from database import get_db
from sqlalchemy.orm import Session
from repository import admin
from database import get_db
import models, oauth2, schemas
from typing import List

router = APIRouter(tags=['admin'], prefix='/admin')


@router.post('/uploadcsv', status_code=status.HTTP_201_CREATED)
def upload_csv(name_in_which_col: int, email_in_which_col: int, css: UploadFile = File(...), db: Session = Depends(get_db)):
    return admin.upload_csv(db, name_in_which_col, email_in_which_col, css)


@router.post('/stage1', status_code=status.HTTP_201_CREATED)
def stage1(request: schemas.Upload, db: Session = Depends(get_db)):
    return admin.stage1(db, request)


@router.get('/stage2',status_code=status.HTTP_201_CREATED)
def stage2(select: int, db: Session = Depends(get_db)):
    return admin.stage2(select, db)


@router.get('/show_all')
def show_all(db: Session = Depends(get_db)):
    return admin.show_all(db)


