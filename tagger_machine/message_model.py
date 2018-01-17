from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()
Base.metadata.schema = 'old_db_models'

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    domain_name = Column(String)

