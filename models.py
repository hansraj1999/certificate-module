from database import Base
from sqlalchemy import Column, Integer, String, DATE


class Upload(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    date_uploaded = Column(DATE)
    by1 = Column(String(50))
    designation1 = Column(String(50))
    by2 = Column(String(50))
    designation2 = Column(String(50))
    certi_for = Column(String(250))
    certi_of = Column(String(50))
    name = Column(String(50))
    email = Column(String(100))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20))
    email = Column(String(50))
    password = Column(String(256))
