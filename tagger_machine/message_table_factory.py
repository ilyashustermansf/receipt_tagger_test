from plugins.database.message_table import MessageTable
from plugins.database.message_table_mock import MessageTableMock
from plugins.database.message_tag_table import MessageTagTable
from plugins.database.message_tag_table_mock import MessageTagTableMock
from testing.configureable_test_mode_mixing import ConfigureableTestModeMixin


class MessageTableFactory(ConfigureableTestModeMixin):
    __message_table = None
    __message_tag_table = None

    def __init__(self, is_test_mode=None):
        super(MessageTableFactory, self).__init__(
            env_variable_name='MESSAGE_DATABASE_MOCK',
            is_test_mode=is_test_mode)

    def get_message_table(self):
        if self.is_test_mode:
            return MessageTableMock()
        else:
            if self.__message_table is None:
                self.__message_table = MessageTable()
            return self.__message_table

    def get_message_tag_table(self):
        if self.is_test_mode:
            return MessageTagTableMock()
        else:
            if self.__message_tag_table is None:
                self.__message_tag_table = MessageTagTable()
            return self.__message_tag_table
