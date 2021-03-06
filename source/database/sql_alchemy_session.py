from __future__ import absolute_import

from database.db_sql_alchemy import DbSqlAlchemy


class SqlAlchemySession(object):
    _cached_sessions = {
        'operations': None,
        'default': None
    }

    @classmethod
    def get_session(cls, connection_name):
        assert connection_name in cls._cached_sessions.keys()
        if cls._cached_sessions[connection_name] is None:
            cls._cached_sessions[connection_name] = SqlAlchemySession(connection_name)
        return cls._cached_sessions[connection_name]

    def __init__(self, connection_name):
        self.connection_name = connection_name
        self.db = DbSqlAlchemy()
        self.db.connect(connection_name)

    def __del__(self):
        self._cached_sessions[self.connection_name] = None
        self.db.disconnect()
