from fastapi import APIRouter, Depends, HTTPException, status , Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from routers import token
import database
import models
import schemas
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.responses import JSONResponse
import random

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not (user.password == request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/logout')
def logout():
    return "Log out called"


@router.post('/create_admin_stage1')
async def create_admin_stage1(email: schemas.EmailSchema, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == email.email).first()

    if not user:
        query = db.query(models.Otp.email, models.Otp.flags).filter(models.Otp.email == email.email).first()

        if not query:
            gen_otp = random.randint(1000, 9999)
            new = models.Otp(email=email.email, otp=gen_otp, flags=1)
            db.add(new)
            db.commit()
            db.refresh(new)
            await mail(email, gen_otp)

        elif query['flags'] < 3:
            gen_otp = random.randint(1000, 9999)
            db.query(models.Otp).filter(models.Otp.email == email.email).update({models.Otp.flags: (query['flags'] + 1), models.Otp.otp: gen_otp}, synchronize_session=False)
            db.commit()
            await mail(email, gen_otp)

        else:
            return False

        return True

    else:
        return f'{email.email} already exits'


@router.post('/create_admin_stage2')
async def create_admin_stage2(email: str, gen_otp: int, db: Session = Depends(database.get_db)):
    query = db.query(models.Otp.email, models.Otp.otp).filter(models.Otp.email == email).first()

    if not query:
        return False # email don't exists

    elif int(query['otp']) == gen_otp:
        db.query(models.Otp).filter(models.Otp.email == email).update(
            {models.Otp.valid: 1}, synchronize_session=False)
        db.commit()
        return True

    else:
        return False


@router.post('/create_admin_stage3', response_model=schemas.CreateUser)
def create_admin_stage3(request: schemas.CreateUser, db: Session = Depends(database.get_db)):
    query = db.query(models.Otp.valid).filter(models.Otp.email == request.email).first()
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if query['valid'] == 1 and not user:
        new_user = models.User(name=request.name, email=request.email, password=request.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    else:
        return False # not a verified account


@router.get('/{id}', response_model=schemas.ShowUser)
def get_admin(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=False)
    return user


async def mail(email: schemas.EmailSchema, otp):
    conf = ConnectionConfig(
        MAIL_USERNAME="certificatemodule@gmail.com",
        MAIL_FROM="certificatemodule@gmail.com",
        MAIL_PASSWORD="algebra@123",
        MAIL_PORT=587,
        MAIL_SERVER="smtp.gmail.com",
        MAIL_TLS=True,
        MAIL_SSL=False
    )

    message = MessageSchema(
        subject="Otp for Certificate-Module",
        recipients=[email.email],
        body=f'Your one time password is {otp} for certificate-module',
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})

