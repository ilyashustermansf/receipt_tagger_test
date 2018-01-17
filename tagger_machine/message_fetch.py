from plugins.database.message_table import MessageTable


class MessageFetch(object):

    def __init__(self, num_messages, start):
        self.num_messages = num_messages
        self.start = start

    def load_messages(self):
        return MessageTable().get_messages(self.num_messages, self.start)

