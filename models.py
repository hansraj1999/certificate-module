from database.database import Base
from sqlalchemy import Column, Integer, String, DATE


class Upload(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    date_uploaded = Column(DATE)
    certificate_by = Column(String(50))
    designation1 = Column(String(50))
    certificate_by2 = Column(String(50))
    designation2 = Column(String(50))
    certificate_for = Column(String(250))
    certificate_of = Column(String(50))
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)


class Otp(Base):
    __tablename__ = 'Otp'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50))
    otp = Column(String(6))
    flags = Column(Integer)
    valid = Column(Integer, default=0)
