from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Boolean

Base = declarative_base()
Base.metadata.schema = 'public'

class MessageTag(Base):
    __tablename__ = 'message_tag'

    message_id = Column(Integer, primary_key=True)
    is_receipt = Column(Boolean)

