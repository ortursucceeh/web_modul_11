from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import  Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50), index=True)
    phone = Column(String(50), index=True)
    birhday = Column(Date, index=True)



