from plugins.database.message_table import MessageTable


class MessagesHandler(object):

    def load_messages(self, messages_amount, offset):
        return MessageTable().get_messages(messages_amount, offset)
