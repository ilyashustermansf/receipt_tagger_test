import pandas as pd
from sqlalchemy import tuple_

from message_tag_model import MessageTag
from plugins.database.table_base import TableBase


class MessageTagTable(TableBase):
    TABLE_NAME = 'message_tag'
    COLUMNS = ['message_id', 'is_receipt']

    def __init__(self):
        super(MessageTagTable, self).__init__(self.TABLE_NAME,
                                              self.COLUMNS)

    def get_messages_tags(self, limit=5):
        db_session = self.get_session()
        tags = db_session.query(MessageTag).limit(limit)
        return [
            {'message_id': tag.message_id}
            for tag in tags
        ]

    def insert_tags(self, tags):
        self.insert_data_frame(pd.DataFrame(tags))

    def delete_tags(self, tags):
        tag_ids = [tag['message_id'] for tag in tags]
        db_session = self.get_session()
        stmt = MessageTag.__table__.delete()\
            .where(MessageTag.message_id.in_(tag_ids))
        db_session.execute(stmt)
        db_session.commit()


if __name__ == '__main__':
    MessageTagTable().delete_tags([
        {'message_id': 1222},
        {'message_id': 2525}
    ])