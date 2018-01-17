from plugins.database.message_table import MessageTable


class MessageFetch(object):

    def load_messages(self, messages_amount, start):
        return MessageTable().get_messages(messages_amount, start)
