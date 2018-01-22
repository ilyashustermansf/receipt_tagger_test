#!/usr/bin/env python
import pandas as pd

from database.db_sql_alchemy import DbSqlAlchemy
from database.sql_alchemy_session import SqlAlchemySession


class TableBase(object):
    """
    Base class for MySQL table implementations.
    """
    schema = 'default'

    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns

    def insert_data_frame(self, data_frame):
        assert isinstance(data_frame, pd.DataFrame)
        db = DbSqlAlchemy()
        db.connect()
        data_frame = data_frame.fillna('')
        data_frame.to_sql(con=db.connection,
                          name=self.table_name,
                          if_exists='append',
                          chunksize=10000,
                          index=False)
        db.disconnect()
        return data_frame

    def get_session(self):
        session = SqlAlchemySession.get_session(self.schema)
        return session.db.session