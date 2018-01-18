from plugins.database.message_table import MessageTable
from plugins.database.message_tag_table import MessageTagTable


class MessagesTagHandler(object):
    URL = 'https://files.superfly.com/files/?msg_id='

    def load_messages(self, messages_amount, offset):
        return MessageTable().get_messages(messages_amount, offset)

    def add_tags(self, tags):
        MessageTagTable().insert_tags(tags)

    def get_tags(self, limit):
        return MessageTagTable().get_messages_tags(limit)

    def delete_tags(self, tags):
        MessageTagTable().delete_tags(tags)

    def get_url(self, message_id):
        return '{}{}'.format(self.URL, message_id)

    def add_urls(self, messages):
        return [{
            'url': self.get_url(message_id),
            'message_id': message_id
        } for message_id in messages]

    def get_next_messages(self, messages_updated):
        return MessageTable().get_messages_not_in(messages_updated)


