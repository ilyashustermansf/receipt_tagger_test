from message_table_factory import MessageTableFactory


class MessagesTagHandler(object):
    URL = 'https://files.superfly.com/files/?msg_id='

    def __init__(self, messages_limit):
        self.messages_limit = messages_limit
        table_factory = MessageTableFactory()
        self.message_table = table_factory.get_message_table()
        self.message_tag_table = table_factory.get_message_tag_table()

    def load_messages(self, offset):
        return self.message_table.get_messages(self.messages_limit, offset)

    def add_tags(self, tags):
        self.message_tag_table.insert_tags(tags)

    def get_tags(self, limit):
        return self.message_tag_table.get_messages_tags(limit)

    def delete_tags(self, tags):
        self.message_tag_table.delete_tags(tags)

    def get_url(self, message_id):
        return '{}{}'.format(self.URL, message_id)

    def add_urls(self, messages):
        return [{
            'url': self.get_url(message['id']),
            'id': message['id']
        } for message in messages]

    def get_next_messages(self, messages_updated):
        messages_updated = [msg['id'] for msg in messages_updated]
        return self.message_table.get_messages_not_in(messages_updated,
                                                      self.messages_limit)

