from message_model import Message
from plugins.database.db_sql_alchemy import DbSqlAlchemy
from plugins.database.table_base import TableBase


class UserTable(TableBase):
    TABLE_NAME = 'user'
    COLUMNS = ['id', 'email']

    COLUMNS_NOT_NULL = []
    DATE_COLUMNS = [0]

    def __init__(self):
        super(UserTable, self).__init__(self.TABLE_NAME,
                                        self.COLUMNS,
                                        self.COLUMNS_NOT_NULL,
                                        ['date'],
                                        date_parser=
                                        TableBase.make_date_parser
                                        ('%Y-%m-%d'))