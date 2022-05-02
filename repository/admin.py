from PIL import Image, ImageDraw, ImageFont
from fastapi import HTTPException, status
from fastapi import UploadFile, File
from string import ascii_letters
from sqlalchemy.orm import Session
import csv
import img2pdf
import models
import os
import schemas
import shutil
import textwrap
import pandas as pd
import qrcode

# domain = 'http://127.0.0.1:8000'
domain = 'https://still-harbor-79180.herokuapp.com'


def show_all(db: Session):
    rows = db.query(models.Upload).all()
    return rows


def upload_csv(name_in_which_col: int, email_in_which_col: int, css: UploadFile = File(...)):
    if not css.filename.endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Upload only Csv file")
    else:
        header = [1, 2]
        columns = [name_in_which_col, email_in_which_col]
        check_columns = set(columns)

        if len(check_columns) != len(columns):
            return "Error can have only 2 columns"
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

            with open("css.csv", "w") as file:
                file.truncate(0)
                if header == ['full_name', 'email']:
                    file.writelines('full_name'',' 'email\n')
                else:
                    file.writelines('email'',''full_name\n')

            dataframe.to_csv('css.csv', index=False, mode='a')
            dataframe = pd.read_csv('css.csv')
            converted_csv = dataframe

        if converted_csv.empty:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"error in uploading the csv file")
        return converted_csv, True


def insert_into_db(db: Session, request: schemas.Upload):
    with open("css.csv", "r") as file:
        csv_reader = csv.DictReader(file)
        for get_data in csv_reader:
            new = models.Upload(
                certificate_by=request.certificate_by, designation1=request.designation1, certificate_by2=request.
                certificate_by2, designation2=request.designation2, certificate_for=request.certificate_for,
                certificate_of=request.certificate_of, name=get_data['full_name'], email=get_data['email'])
            db.add(new)
            db.commit()
            db.refresh(new)
    getting_index = db.query(models.Upload.id).order_by(models.Upload.id.desc()).first()
    read_uploaded_csv = pd.read_csv('css.csv')
    no_of_certificates = len(read_uploaded_csv)
    index = int(getting_index['id']) - no_of_certificates + 1
    query = db.query(models.Upload.id, models.Upload.certificate_of, models.Upload.certificate_for, models.Upload.
                     certificate_by, models.Upload.certificate_by2, models.Upload.designation1, models.Upload.
                     designation2, models.Upload.name).filter(models.Upload.id >= index).all()
    return query, True


def generate_certificate(selected_certificate_template_id: int, db: Session):
    if os.path.exists('generated_certificate'):
        shutil.rmtree('generated_certificate/')
        os.mkdir('generated_certificate')
    else:
        os.mkdir('generated_certificate')

    getting_index = db.query(models.Upload.id).order_by(models.Upload.id.desc()).first()
    font_id = 1
    read_uploaded_csv = pd.read_csv('css.csv')
    no_of_certificates = len(read_uploaded_csv)
    index = int(getting_index['id']) - no_of_certificates + 1
    query = db.query(models.Upload.id, models.Upload.certificate_of, models.Upload.certificate_for, models.Upload.
                     certificate_by, models.Upload.certificate_by2, models.Upload.designation1, models.Upload.
                     designation2, models.Upload.name).filter(models.Upload.id >= index).all()

    for row in query:

        unique_id = str(row['id'])
        certificate_of = "OF" + " " + str(row['certificate_of'])
        certificate_for = str(row['certificate_for'])
        certificate_by = str(row['certificate_by'])
        certificate_by_2 = str(row['certificate_by2'])
        designation1 = str(row['designation1'])
        designation2 = str(row['designation2'])
        name = str(row['name'])

        certificate_of = certificate_of.title()
        certificate_for = certificate_for.title()
        certificate_by = certificate_by.title()
        name = name.title()
        designation = designation1.title()
        certificate_by_2 = certificate_by_2.title()
        designation2 = designation2.title()
        certificate_of = certificate_of.upper()

        url = f'{domain}/admin/finds/{unique_id}'
        qr = qrcode.QRCode(box_size=8)
        qr.add_data(url)
        qr.make()
        image_qr = qr.make_image()

        if selected_certificate_template_id == 1:

            img = Image.open('templates/certificate1.png')
            d1 = ImageDraw.Draw(img)
            img.paste(image_qr, (660, 1100))

            my_font = ImageFont.truetype('font/Amsterdam.ttf', 150)
            my_font2 = ImageFont.truetype('font/Poppins-Medium.ttf', 40)
            my_font3 = ImageFont.truetype('font/Poppins-Light.ttf', 24)
            my_font4 = ImageFont.truetype('font/Poppins-Medium.ttf', 30)
            my_font5 = ImageFont.truetype('font/Poppins-Light.ttf', 24)

            avg_char_width = sum(my_font3.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            max_char_count = int((img.size[0] * .95) / avg_char_width - 45)
            scaled_for = textwrap.fill(text=certificate_for, width=max_char_count)

            d1.text((738, 690), name, font=my_font, fill=(209, 182, 86), anchor='mm')
            d1.text((1080, 327), certificate_of, font=my_font2, fill=(0, 0, 0), anchor='mm')
            d1.text((750, 896), scaled_for, font=my_font3, fill=(0, 0, 0), anchor='mm', align='right')
            d1.text((314, 1214), certificate_by, font=my_font4, fill=(0, 0, 0), anchor='mm')
            d1.text((314, 1257), designation, font=my_font5, fill=(209, 182, 86), anchor='mm')
            d1.text((1215, 1211), certificate_by_2, font=my_font4, fill=(0, 0, 0), anchor='mm')
            d1.text((1215, 1260), designation2, font=my_font5, fill=(209, 182, 86), anchor='mm')

            reduced_size = img.resize((1000, 707))
            reduced_size.save(f"generated_certificate/{unique_id}_generated_certificate.png")

        elif selected_certificate_template_id == 2:

            img = Image.open('templates/certificate2.png')
            d1 = ImageDraw.Draw(img)
            qr2 = qrcode.QRCode(box_size=18)
            qr2.add_data(url)
            qr2.make()
            img_qr2 = qr2.make_image()
            img.paste(img_qr2, (2450, 3000))

            my_font2 = ImageFont.truetype('font/Montserrat-Medium.ttf', 85)
            my_font3 = ImageFont.truetype('font/Montserrat-SemiBold.ttf', 85)
            my_font4 = ImageFont.truetype('font/Montserrat-Medium.ttf', 85)

            avg_char_width = sum(my_font2.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            max_char_count = int((img.size[0] * .95) / avg_char_width)
            scaled_for = textwrap.fill(text=certificate_for, width=max_char_count - 30)

            if font_id == 1:
                my_font = ImageFont.truetype('font/AlexBrush-Regular.ttf', 400)
                d1.text((2761, 1750), name, font=my_font, fill=(87, 84, 81), anchor='mm')

            elif font_id == 2:
                my_font = ImageFont.truetype('font/Alegreya-Black.ttf', 300)
                d1.text((2761, 1750), name, font=my_font, fill=(87, 84, 81), anchor='mm')

            d1.text((2761, 2120), scaled_for, font=my_font2, fill=(87, 84, 81), anchor='mm')
            d1.text((1382, 3295), certificate_by, font=my_font3, fill=(87, 84, 81), anchor='mm')
            d1.text((1382, 3437), designation, font=my_font4, fill=(90, 84, 81), anchor='mm')
            d1.text((4410, 3295), certificate_by_2, font=my_font3, fill=(87, 84, 81), anchor='mm')
            d1.text((4410, 3437), designation2, font=my_font4, fill=(90, 84, 81), anchor='mm')
            reduced_size = img.resize((1056*3, 816*3))
            reduced_size.save(f"generated_certificate/{unique_id}_generated_certificate.png")

        elif selected_certificate_template_id == 3:

            img = Image.open('templates/certificate3.png')
            d1 = ImageDraw.Draw(img)
            img.paste(image_qr, (1050, 1000))

            my_font2 = ImageFont.truetype('font/league-gothic.regular.ttf', 85)
            my_font3 = ImageFont.truetype('font/league-gothic.regular.ttf', 140)
            my_font4 = ImageFont.truetype('font/Montserrat-Light.ttf', 20)
            my_font5 = ImageFont.truetype('font/league-gothic.regular.ttf', 40)
            my_font6 = ImageFont.truetype('font/league-gothic.regular.ttf', 28)

            avg_char_width = sum(my_font4.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            max_char_count = int((img.size[0] * .95) / avg_char_width)
            scaled_for = textwrap.fill(text=certificate_for, width=max_char_count - 55)

            d1.text((1208, 270), certificate_of, font=my_font2, fill=(255, 157, 43), anchor='mm')
            d1.text((1208, 650), name, font=my_font3, fill=(255, 157, 43), anchor='mm')
            d1.text((1208, 770), scaled_for, font=my_font4, fill=(0, 0, 0), anchor='mm')
            d1.text((720, 1174), certificate_by, font=my_font5, fill=(255, 157, 43), anchor='mm')
            d1.text((720, 1214), designation, font=my_font6, fill=(0, 0, 0), anchor='mm')
            d1.text((1584, 1174), certificate_by_2, font=my_font5, fill=(255, 157, 43), anchor='mm')
            d1.text((1584, 1214), designation2, font=my_font6, fill=(0, 0, 0), anchor='mm')
            d1.text((1800, 200), unique_id, font=my_font6, fill=(255, 157, 43), anchor='mm')

            reduced_size = img.resize((1000, 707))
            reduced_size.save(f"generated_certificate/{unique_id}_generated_certificate.png")

        elif selected_certificate_template_id == 4:
            img = Image.open('templates/certificate4.png')
            d1 = ImageDraw.Draw(img)
            img.paste(image_qr, (0, 1130))

            my_font = ImageFont.truetype('font/Montserrat-ExtraBold.ttf', 50)
            my_font3 = ImageFont.truetype('font/Montserrat-Medium.ttf', 30)
            my_font4 = ImageFont.truetype('font/Montserrat-SemiBold.ttf', 30)
            my_font5 = ImageFont.truetype('font/Montserrat-Medium.ttf', 20)

            if font_id == 1:
                my_font2 = ImageFont.truetype('font/Virtual-Regular.ttf', 180)
                d1.text((1170, 700), name, font=my_font2, fill=(255, 255, 255), anchor='mm', align='center')

            elif font_id == 2:
                my_font2 = ImageFont.truetype('font/Montserrat-SemiBold.ttf', 70)
                d1.text((1170, 730), name, font=my_font2, fill=(255, 255, 255), anchor='mm')

            avg_char_width = sum(my_font3.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            max_char_count = int((img.size[0] * .95) / avg_char_width)

            scaled_for = textwrap.fill(text=certificate_for, width=max_char_count - 26)

            d1.text((1170, 422), certificate_of, font=my_font, fill=(255, 255, 255), anchor='mm')
            d1.text((1190, 840), scaled_for, font=my_font3, fill=(255, 255, 255), anchor='mm')
            d1.text((1612, 1202), certificate_by, font=my_font4, fill=(255, 255, 255), anchor='mm')
            d1.text((1612, 1241), designation, font=my_font5, fill=(41, 169, 225), anchor='mm')
            d1.text((746, 1202), certificate_by_2, font=my_font4, fill=(255, 255, 225), anchor='mm')
            d1.text((746, 1241), designation2, font=my_font5, fill=(41, 169, 225), anchor='mm')
            reduced_size = img.resize((1000, 707))
            reduced_size.save(f"generated_certificate/{unique_id}_generated_certificate.png")

        else:
            return "Template not found"

    with open("css.csv", "w") as f:
        f.truncate(0)
    return True


def find(u_id, db: Session):
    query = db.query(models.Upload.id, models.Upload.certificate_of, models.Upload.certificate_for, models.Upload.
                     certificate_by, models.Upload.certificate_by2, models.Upload.designation1, models.Upload.
                     designation2, models.Upload.name).filter(models.Upload.id == u_id).first()
    if not query:
        return 'Not Found'
    else:
        return query


def finds(u_id, db: Session):
    query = db.query(models.Upload.id, models.Upload.certificate_of, models.Upload.certificate_for, models.Upload.
                     certificate_by, models.Upload.certificate_by2, models.Upload.designation1, models.Upload.
                     designation2, models.Upload.name).filter(models.Upload.id == int(u_id)).first()

    if not query:
        return {'response': 'Error 404 Not Found'}
    else:
        return f"{u_id} exists with the following details : "\
               f" ID = {query['id']}" \
               f" Certificate Given to = {str(query['name'])}," \
               f" Certificate of = {str(query['certificate_of'])}," \
               f" Certificate for = {str(query['certificate_for'])}," \
               f" Certificate By = {str(query['certificate_by'])}," \
               f" Certificate By2 = {str(query['certificate_by2'])}," \



def download():
    if os.path.exists('generated_certificate'):
        with open("output/Images.pdf", "wb") as f:
            f.write(img2pdf.convert(['generated_certificate/'+i[0:] for i in os.listdir('generated_certificate/') if i.
                                    endswith(".png")]))
            return 'output/Images.pdf'


def delete(u_id, db: Session):
    if find(u_id, db) != 'Not Found':
        db.query(models.Upload).filter(models.Upload.id == u_id).delete()
        db.commit()

        return 'User Deleted'
    else:
        return f'{u_id} Not Exists'


def update(u_id, name, db: Session):
    if find(u_id, db) != 'Not Found':
        db.query(models.Upload).filter(models.Upload.id == u_id).update({models.Upload.name: name})
        db.commit()
        return 'User Updated'
    else:
        return f'{u_id} Not Exists'


def specific_download(u_id, db: Session):
    query = db.query(models.Upload.id, models.Upload.certificate_of, models.Upload.certificate_for, models.Upload.
                     certificate_by, models.Upload.certificate_by2, models.Upload.designation1, models.Upload.
                     designation2, models.Upload.name).filter(models.Upload.id == int(u_id)).first()
    if os.path.exists('generated_certificate'):
        shutil.rmtree('generated_certificate/')
        os.mkdir('generated_certificate')
    else:
        os.mkdir('generated_certificate')
    if not query:
        return {'response': False}
    else:
        unique_id = str(query['id'])
        certificate_of = str(query['certificate_of'])
        certificate_for = str(query['certificate_for'])
        certificate_by = str(query['certificate_by'])
        certificate_by2 = str(query['certificate_by2'])
        designation1 = str(query['designation1'])
        designation2 = str(query['designation2'])
        name = str(query['name'])
        certificate_of = certificate_of.title()
        certificate_for = certificate_for.title()
        certificate_by = certificate_by.title()
        name = name.title()
        designation = designation1.title()
        certificate_by2 = certificate_by2.title()
        designation2 = designation2.title()
        url = f'{domain}/admin/finds/{u_id}'
        qr = qrcode.QRCode(box_size=8)
        qr.add_data(url)
        qr.make()
        img_qr = qr.make_image()

        img = Image.open('templates/certificate3.png')
        d1 = ImageDraw.Draw(img)
        img.paste(img_qr, (1050, 1000))

        certificate_of = "CERTIFICATE OF" + " " + certificate_of.upper()
        name = name.upper()
        certificate_by = certificate_by.upper()
        certificate_by2 = certificate_by2.upper()
        designation = designation.upper()
        designation2 = designation2.upper()

        my_font2 = ImageFont.truetype('font/league-gothic.regular.ttf', 85)
        my_font3 = ImageFont.truetype('font/league-gothic.regular.ttf', 140)
        my_font4 = ImageFont.truetype('font/Montserrat-Light.ttf', 20)
        my_font5 = ImageFont.truetype('font/league-gothic.regular.ttf', 40)
        my_font6 = ImageFont.truetype('font/league-gothic.regular.ttf', 28)

        avg_char_width = sum(my_font4.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        max_char_count = int((img.size[0] * .95) / avg_char_width)
        scaled_for = textwrap.fill(text=certificate_for, width=max_char_count - 55)

        d1.text((1208, 270), certificate_of, font=my_font2, fill=(255, 157, 43), anchor='mm')
        d1.text((1208, 650), name, font=my_font3, fill=(255, 157, 43), anchor='mm')
        d1.text((1208, 770), scaled_for, font=my_font4, fill=(0, 0, 0), anchor='mm')
        d1.text((720, 1174), certificate_by, font=my_font5, fill=(255, 157, 43), anchor='mm')
        d1.text((720, 1214), designation, font=my_font6, fill=(0, 0, 0), anchor='mm')
        d1.text((1584, 1174), certificate_by2, font=my_font5, fill=(255, 157, 43), anchor='mm')
        d1.text((1584, 1214), designation2, font=my_font6, fill=(0, 0, 0), anchor='mm')
        d1.text((1800, 200), unique_id, font=my_font6, fill=(255, 157, 43), anchor='mm')

        reduced_size = img.resize((1000, 707))
        reduced_size.save(f"generated_certificate/{unique_id}_generated_certificate.png")
        return download()
