import schemas
from database import get_db
from sqlalchemy.orm import Session
import models
from fastapi import HTTPException, status
import csv
import pandas as pd
from fastapi import UploadFile, File


def upload_csv(db: Session, name_in_which_col: int, email_in_which_col: int, css: UploadFile = File(...)):
    if not css.filename.endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Upload only Csv file")
    else:

        header = [1, 2]
        temp = [name_in_which_col, email_in_which_col]
        temp_set = set(temp)

        if len(temp_set) != len(temp):
            return "error can have only 2 columns"

        else:
            dataframe = pd.read_csv(css.file, index_col=False, delimiter=',')

            if name_in_which_col == 1:
                header[0] = 'full_name'
            elif name_in_which_col == 2:
                header[1] = 'full_name'
            if email_in_which_col == 1:
                header[0] = 'email'
            elif email_in_which_col == 2:
                header[1] = 'email'
            dataframe.to_csv('css.csv', index=False, header=header)
            dataframe = pd.read_csv('css.csv')
            converted_csv = dataframe

        if converted_csv.empty:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"error in uploading the csv file")

        return converted_csv


def stage1(db: Session, request: schemas.Upload):
    with open("css.csv", "r") as f:
        csv_reader = csv.DictReader(f)
        for get_data in csv_reader:
            new = models.Upload(
                by1=request.by1, designation1=request.designation1, by2=request.by2,
                designation2=request.designation2, certi_for=request.certi_for,
                certi_of=request.certi_of, name=get_data['full_name'], email=get_data['email'])
            db.add(new)
            db.commit()
            db.refresh(new)

    return "Successfully Uploaded"


def stage2(select: int, db: Session):
    pass
