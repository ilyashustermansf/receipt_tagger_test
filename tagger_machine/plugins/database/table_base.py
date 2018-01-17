#!/usr/bin/env python
import pandas as pd
from datetime import datetime
from tagger_machine.plugins.database.db_sql_alchemy import DbSqlAlchemy


class TableBase(object):
    """
    Base class for MySQL table implementations.
    """

    @staticmethod
    def make_date_parser(date_format):
        def date_parser(date_string):
            return datetime.strptime(date_string, date_format)

        return date_parser

    def __init__(self, table_name, columns, columns_not_null, date_columns,
                 round_columns=None, date_parser=None):
        self.table_name = table_name
        self.columns = columns
        self.columns_not_null = columns_not_null
        self.date_columns_index = date_columns
        self.round_columns = round_columns
        self.date_parser = date_parser


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
