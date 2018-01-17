#!/usr/bin/env python
import pandas as pd
from datetime import datetime
from tagger_machine.plugins.database.db_sql_alchemy import DbSqlAlchemy


class TableBase(object):
    """
    Base class for MySQL table implementations.
    """

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
