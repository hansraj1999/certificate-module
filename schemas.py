from pydantic import BaseModel
from typing import Optional

class UploadBase(BaseModel):
    id: int
    date_uploaded: str
    by1: str
    designation1: str
    by2: str
    designation2: str
    certi_for: str
    certi_of: str
    name: str


class Upload(BaseModel):
    date_uploaded: str
    by1: str
    designation1: str
    by2: str
    designation2: str
    certi_for: str
    certi_of: str

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None