from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import _mysql_connector
import sqlite3

SQLALCHAMY_DB_URL = 'sqlite:///./data.db'
engine = create_engine(SQLALCHAMY_DB_URL, connect_args={'check_same_thread': False})

#SQLALCHAMY_DB_URL = 'mysql+mysqlconnector://root:root@localhost:3306/main'
# engine = create_engine(SQLALCHAMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
