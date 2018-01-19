from message_model import Message
from plugins.database.sql_alchemy_session import SqlAlchemySession
from plugins.database.table_base import TableBase


class MessageTable(TableBase):
    TABLE_NAME = 'messages'
    COLUMNS = ['id', 'domain_name']

    def __init__(self):
        super(MessageTable, self).__init__(self.TABLE_NAME,
                                           self.COLUMNS)

    def get_messages(self, num_messages, offset):
        db_session = self.get_session()
        messages = db_session.query(Message).limit(num_messages).offset(
            offset)
        return self.dictify_messages(messages)

    def get_messages_not_in(self, messages_updated):
        db_session = self.get_session()
        messages = db_session.query(Message).\
            filter(~Message.id.in_(messages_updated))
        return self.dictify_messages(messages)

    def dictify_messages(self, messages):
        return [
            {'id': message.id}
            for message in messages
        ]
