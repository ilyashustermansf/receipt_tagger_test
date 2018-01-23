import logging

from message_table_factory import MessageTableFactory
from common.persistence_utils import get_message_content


def change_tag_to_message_dict(tag):
    return {'id': tag['message_id']}


class MessagesTagHandler(object):
    URL = 'https://files.superfly.com/files/?msg_id='
    logging.basicConfig(format=logging.INFO)

    def __init__(self, messages_limit):
        logging.info('Initiating Tag Handler')
        self.messages_limit = messages_limit
        table_factory = MessageTableFactory()
        self.message_table = table_factory.get_message_table()
        self.message_tag_table = table_factory.get_message_tag_table()

    def load_messages(self, offset):
        logging.info('Loading messages limit={} offset={}'.format(
            self.messages_limit,
            offset))
        return self.message_table.get_messages(self.messages_limit, offset)

    def add_tags(self, tags):
        logging.info('Requested Adding tags={}'.format(tags))
        all_tags = [tag['message_id'] for tag
                    in self.get_tags()]
        tags = [tag for tag in tags if tag['message_id'] not in all_tags]
        logging.info('Adding Tags after triming tag '
                     'existed tags={}'.format(tags))
        self.message_tag_table.insert_tags(tags)
        logging.info('Inserted tags Successfully!')

    def get_tags(self, limit=None):
        if limit is None:
            logging.info('Requested all tags..')
            return self.message_tag_table.get_all_tags()
        else:
            logging.info('Requested all tags')
            return self.message_tag_table.get_messages_tags(limit)

    def delete_tags(self, tags):
        logging.info('Deleting tags...')
        self.message_tag_table.delete_tags(tags)

    def get_url(self, message_id):
        return '{}{}'.format(self.URL, message_id)

    def add_urls(self, messages):
        messages_with_urls = [
            {
                'url': self.get_url(message['id']),
                'id': message['id']
            } for message in messages]
        logging.info('Adding urls to messages={}'.format(messages_with_urls))
        return messages_with_urls

    def get_messages_not_in(self, messages_updated):
        logging.info('Get Messages not in ={}'.format(messages_updated))
        messages_updated = [msg['id'] for msg in messages_updated]
        return self.message_table.get_messages_not_in(messages_updated,
                                                      self.messages_limit)

    def get_next_messages(self):
        logging.info('Get Next messages...')
        messages_tagged = self.message_tag_table.get_all_tags()
        messages_tagged = list(map(change_tag_to_message_dict, messages_tagged))
        next_messages = self.get_messages_not_in(messages_tagged)
        logging.info('Loaded next messages={}'.format(next_messages))
        return next_messages

    def get_html_content(self, message_id):
        return get_message_content(message_id)

    def get_next_messages_with_content(self):
        return [{
            'content': self.get_html_content(message['id']),
            'id': message['id']
        } for message in self.get_next_messages()]
