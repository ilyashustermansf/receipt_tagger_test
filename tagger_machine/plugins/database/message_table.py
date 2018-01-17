import numpy as np

from message_model import Message
from plugins.database.sql_alchemy_session import SqlAlchemySession
from plugins.database.table_base import TableBase


class MessageTable(TableBase):
    TABLE_NAME = 'messages'
    COLUMNS = ['id', 'domain_name']

    def __init__(self):
        super(MessageTable, self).__init__(self.TABLE_NAME,
                                        self.COLUMNS)

    def get_messages(self, num_messages, start):
        session = SqlAlchemySession.get_session()
        db_session = session.db.session
        message = db_session.query(Message).first()
        print(message.id)
        return np.random.randint(-6,8,49)