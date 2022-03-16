from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi import UploadFile, File
from PIL import Image, ImageDraw, ImageFont
from string import ascii_letters
import schemas
import models
import csv
import textwrap
import pandas as pd


def show_all(db: Session):
    rows = db.query(models.Upload).all()
    return rows


def upload_csv(name_in_which_col: int, email_in_which_col: int, css: UploadFile = File(...)):
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

            with open("css.csv", "w") as f:
                f.truncate(0)
                if header == ['full_name', 'email']:
                    f.writelines('full_name'',' 'email\n')
                else:
                    f.writelines('email'',''full_name\n')

            dataframe.to_csv('css.csv', index=False, mode='a')
            dataframe = pd.read_csv('css.csv')
            converted_csv = dataframe

        if converted_csv.empty:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"error in uploading the csv file")
        return {'response': 'True'}


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

    return 'sucessfull'


def stage2(ceri_template: int, db: Session):
    geting_index = db.query(models.Upload.id).order_by(models.Upload.id.desc()).first()
    font_id = 1
    certi = pd.read_csv('css.csv')
    no_of_certi=len(certi)
    index = int(geting_index['id'])-no_of_certi+1
    querry = db.query(models.Upload.id, models.Upload.certi_of, models.Upload.certi_for, models.Upload.by1, models.Upload.by2
                    , models.Upload.designation1, models.Upload.designation2, models.Upload.name).filter(models.Upload.id >= index).all()

    for i in querry:

        u_id = str(i['id'])
        certi_of = str(i['certi_of'])
        for_ = str(i['certi_for'])
        by1 = str(i['by1'])
        by2 = str(i['by2'])
        designation1 = str(i['designation1'])
        designation2 = str(i['designation2'])
        name = str(i['name'])
        certi_of = certi_of.title()
        for_ = for_.title()
        by = by1.title()
        name = name.title()
        designation = designation1.title()
        by2 = by2.title()
        designation2 = designation2.title()

        if ceri_template == 1:
            # This method returns the image object.

            img = Image.open('templates/certi1.png')
            d1 = ImageDraw.Draw(img)
            certi_of = "OF" + " " + certi_of.upper()

            myFont = ImageFont.truetype('font/Amsterdam.ttf', 150)
            myFont2 = ImageFont.truetype('font/Poppins-Medium.ttf', 40)
            myFont3 = ImageFont.truetype('font/Poppins-Light.ttf', 24)
            myFont4 = ImageFont.truetype('font/Poppins-Medium.ttf', 30)
            myFont5 = ImageFont.truetype('font/Poppins-Light.ttf', 24)

            avg_char_width = sum(myFont3.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            max_char_count = int((img.size[0] * .95) / avg_char_width - 45)
            scaled_for = textwrap.fill(text=for_, width=max_char_count)

            d1.text((738, 690), name, font=myFont, fill=(209, 182, 86), anchor='mm')
            d1.text((1080, 327), certi_of, font=myFont2, fill=(0, 0, 0), anchor='mm')
            d1.text((750, 896), scaled_for, font=myFont3, fill=(0, 0, 0), anchor='mm', align='right')
            d1.text((314, 1214), by, font=myFont4, fill=(0, 0, 0), anchor='mm')
            d1.text((314, 1257), designation, font=myFont5, fill=(209, 182, 86), anchor='mm')
            d1.text((1215, 1211), by2, font=myFont4, fill=(0, 0, 0), anchor='mm')
            d1.text((1215, 1260), designation2, font=myFont5, fill=(209, 182, 86), anchor='mm')
            img.save(f"generated_certi/{u_id}gen_certi.png")

        elif ceri_template == 2:

            img = Image.open('templates/certi2.png')
            d1 = ImageDraw.Draw(img)

            myFont2 = ImageFont.truetype('font/Montserrat-Medium.ttf', 85)
            myFont3 = ImageFont.truetype('font/Montserrat-SemiBold.ttf', 85)
            myFont4 = ImageFont.truetype('font/Montserrat-Medium.ttf', 85)

            avg_char_width = sum(myFont2.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            max_char_count = int((img.size[0] * .95) / avg_char_width)
            scaled_for = textwrap.fill(text=for_, width=max_char_count - 30)

            if font_id == 1:
                myFont = ImageFont.truetype('font/AlexBrush-Regular.ttf', 400)
                d1.text((2761, 1750), name, font=myFont, fill=(87, 84, 81), anchor='mm')

            elif font_id == 2:
                myFont = ImageFont.truetype('font/Alegreya-Black.ttf', 300)
                d1.text((2761, 1750), name, font=myFont, fill=(87, 84, 81), anchor='mm')

            d1.text((2761, 2120), scaled_for, font=myFont2, fill=(87, 84, 81), anchor='mm')
            d1.text((1382, 3295), by, font=myFont3, fill=(87, 84, 81), anchor='mm')
            d1.text((1382, 3437), designation, font=myFont4, fill=(90, 84, 81), anchor='mm')
            d1.text((4410, 3295), by2, font=myFont3, fill=(87, 84, 81), anchor='mm')
            d1.text((4410, 3437), designation2, font=myFont4, fill=(90, 84, 81), anchor='mm')

            img.save(f"generated_certi/{u_id}gen_certi.png")

        elif ceri_template == 3:

            img = Image.open('templates/certi3.png')
            d1 = ImageDraw.Draw(img)

            certi_of = "CERTIFICATE OF" + " " + certi_of.upper()
            name = name.upper()
            by = by.upper()
            by2 = by2.upper()
            designation = designation.upper()
            designation2 = designation2.upper()

            myFont2 = ImageFont.truetype('font/league-gothic.regular.ttf', 85)
            myFont3 = ImageFont.truetype('font/league-gothic.regular.ttf', 140)
            myFont4 = ImageFont.truetype('font/Montserrat-Light.ttf', 20)
            myFont5 = ImageFont.truetype('font/league-gothic.regular.ttf', 40)
            myFont6 = ImageFont.truetype('font/league-gothic.regular.ttf', 28)

            avg_char_width = sum(myFont4.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            max_char_count = int((img.size[0] * .95) / avg_char_width)
            scaled_for = textwrap.fill(text=for_, width=max_char_count - 55)

            d1.text((1208, 270), certi_of, font=myFont2, fill=(255, 157, 43), anchor='mm')
            d1.text((1208, 650), name, font=myFont3, fill=(255, 157, 43), anchor='mm')
            d1.text((1208, 770), scaled_for, font=myFont4, fill=(0, 0, 0), anchor='mm')
            d1.text((720, 1174), by, font=myFont5, fill=(255, 157, 43), anchor='mm')
            d1.text((720, 1214), designation, font=myFont6, fill=(0, 0, 0), anchor='mm')
            d1.text((1584, 1174), by2, font=myFont5, fill=(255, 157, 43), anchor='mm')
            d1.text((1584, 1214), designation2, font=myFont6, fill=(0, 0, 0), anchor='mm')

            img.save(f"generated_certi/{u_id}gen_certi.png")


        elif ceri_template == 4:

            img = Image.open('templates/certi4.png')
            d1 = ImageDraw.Draw(img)
            certi_of = "Of " + certi_of.upper()

            myFont = ImageFont.truetype('font/Montserrat-ExtraBold.ttf', 50)
            myFont3 = ImageFont.truetype('font/Montserrat-Medium.ttf', 30)
            myFont4 = ImageFont.truetype('font/Montserrat-SemiBold.ttf', 30)
            myFont5 = ImageFont.truetype('font/Montserrat-Medium.ttf', 20)

            if font_id == 1:
                myFont2 = ImageFont.truetype('font/Virtual-Regular.ttf', 180)
                d1.text((1170, 700), name, font=myFont2, fill=(255, 255, 255), anchor='mm', align='center')

            elif font_id == 2:
                myFont2 = ImageFont.truetype('font/Montserrat-SemiBold.ttf', 70)
                d1.text((1170, 730), name, font=myFont2, fill=(255, 255, 255), anchor='mm')

            avg_char_width = sum(myFont3.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            max_char_count = int((img.size[0] * .95) / avg_char_width)

            scaled_for = textwrap.fill(text=for_, width=max_char_count - 26)

            d1.text((1170, 422), certi_of, font=myFont, fill=(255, 255, 255), anchor='mm')
            d1.text((1190, 840), scaled_for, font=myFont3, fill=(255, 255, 255), anchor='mm')
            d1.text((1612, 1202), by, font=myFont4, fill=(255, 255, 255), anchor='mm')
            d1.text((1612, 1241), designation, font=myFont5, fill=(41, 169, 225), anchor='mm')
            d1.text((746, 1202), by2, font=myFont4, fill=(255, 255, 225), anchor='mm')
            d1.text((746, 1241), designation2, font=myFont5, fill=(41, 169, 225), anchor='mm')

            img.save(f"generated_certi/{u_id}_gen_certi.png")
            return f'generated_certi/{u_id}_gen_certi.png'
        else:
            return "Template not found"

    with open("css.csv", "w") as f:
        f.truncate(0)

    return f'generated_certi/{u_id}_gen_certi.png'



