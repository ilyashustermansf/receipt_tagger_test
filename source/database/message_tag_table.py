import pandas as pd

from database.table_base import TableBase
from message_tag_model import MessageTag


class MessageTagTable(TableBase):
    TABLE_NAME = 'message_tags'
    SCHEMA = 'operations'
    COLUMNS = ['message_id', 'is_receipt']

    def __init__(self):
        super(MessageTagTable, self).__init__(self.TABLE_NAME,
                                              self.COLUMNS)
        self.db_session = self.get_session()

    def get_messages_tags(self, limit=5):
        db_session = self.db_session
        tags = db_session.query(MessageTag).limit(limit)
        return self.dictify_tags(tags)

    def dictify_tags(self, tags):
        return [
            {'message_id': tag.message_id,
             'is_receipt': tag.is_receipt}
            for tag in tags
        ]

    def insert_tags(self, tags):
        self.insert_data_frame(pd.DataFrame(tags))

    def delete_tags(self, tag_ids):
        db_session = self.db_session
        statement = MessageTag.__table__.delete() \
            .where(MessageTag.message_id.in_(tag_ids))
        db_session.execute(statement)
        db_session.commit()

    def get_all_tags(self, limit=None):
        db_session = self.db_session
        tags = db_session.query(MessageTag)
        if limit is not None:
            tags = tags.limit(limit)
        else:
            tags = tags.all()
        return self.dictify_tags(tags)


if __name__ == '__main__':
    MessageTagTable().delete_tags([
        {'message_id': 1222},
        {'message_id': 2525}
    ])
