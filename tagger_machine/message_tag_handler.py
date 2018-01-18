from plugins.database.message_table import MessageTable
from plugins.database.message_tag_table import MessageTagTable


class MessagesTagHandler(object):

    def load_messages(self, messages_amount, offset):
        return MessageTable().get_messages(messages_amount, offset)

    def add_tags(self, tags):
        MessageTagTable().insert_tags(tags)

    def get_tags(self, limit):
        return MessageTagTable().get_messages_tags(limit)

    def delete_tags(self, tags):
        MessageTagTable().delete_tags(tags)
