from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    date = Column(Date)
