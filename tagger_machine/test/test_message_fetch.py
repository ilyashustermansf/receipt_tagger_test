from unittest import TestCase, skip
import numpy as np
from tagger_machine.message_tag_handler import MessagesTagHandler


class TestMessageFetch(TestCase):

    def setUp(self):
        self.message_handler = MessagesTagHandler(messages_limit=50)
        self.tags = [{'message_id': 1222, 'is_receipt': False},
                     {'message_id': 2525, 'is_receipt': True}]
        self.messages = [{'id': 2698406951}, {'id': 2698406952},
                         {'id': 2698406953},
                         {'id': 2698406954}, {'id': 2698407037},
                         {'id': 2577499155}, {'id': 2577499203},
                         {'id': 2698406966},
                         {'id': 2698406967}, {'id': 2698407206}]

    @skip
    def test_load_fifty_messages(self):
        messages = self.message_handler.load_messages(offset=2)
        self.assertTrue(len(messages) == 50, msg=messages)

    @skip
    def test_offset_messages_from_database(self):
        message_offset_one = \
            self.message_handler.load_messages(offset=1)[1]
        message_offset_two = \
            self.message_handler.load_messages(offset=2)[0]
        self.assertEqual(message_offset_one['id'], message_offset_two['id'])

    @skip
    def test_delete_tags(self):
        self.message_handler.delete_tags(self.tags)

    @skip
    def test_add_two_answers_and_delete(self):
        tag = self.tags[0]
        tag2 = self.tags[1]
        self.message_handler.add_tags([tag, tag2])
        tags = self.message_handler.get_tags(limit=2)
        self.assertEqual(tags[0]['message_id'], tag['message_id'])
        self.assertEqual(tags[1]['message_id'], tag2['message_id'])
        self.message_handler.delete_tags([tag, tag2])

    def test_get_message_url(self):
        message_id = 1234
        url = self.message_handler.get_url(message_id)
        self.assertEqual(url,
                         'https://files.superfly.com/files/?msg_id={}'
                         .format(message_id))

    def test_get_messages_urls(self):
        messages_with_urls = self.message_handler.add_urls(self.messages)
        for message, message_with_url in zip(self.messages,
                                             messages_with_urls):
            self.assertEqual(message_with_url['url'],
                             'https://files.superfly.com/files/?msg_id={}'
                             .format(message['id']))
            self.assertTrue('id' in message_with_url)

    @skip
    def test_get_next_messages_from_already_tagged_messages(self):
        tagged_messages = self.messages
        next_messages = [msg['id'] for msg in
                         self.message_handler.get_next_messages(
                             tagged_messages)]
        zero_messages = [msg_id for msg_id in next_messages
                         if msg_id in tagged_messages]
        self.assertTrue(len(zero_messages) == 0, zero_messages)
