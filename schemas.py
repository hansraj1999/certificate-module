from pydantic import BaseModel


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

