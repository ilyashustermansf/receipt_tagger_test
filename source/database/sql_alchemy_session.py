from __future__ import absolute_import

from database.db_sql_alchemy import DbSqlAlchemy


class SqlAlchemySession(object):
    _cached_session = None

    @classmethod
    def get_session(cls, connection_name):
        if not cls._cached_session:
            cls._cached_session = SqlAlchemySession(connection_name)
        return cls._cached_session

    def __init__(self, connection_name):
        self.db = DbSqlAlchemy()
        self.db.connect(connection_name)

    def __del__(self):
        self._cached_session = None
        self.db.disconnect()
