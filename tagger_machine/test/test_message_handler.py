import copy
from unittest import TestCase, skip
import os
from tagger_machine.message_tag_handler import MessagesTagHandler


class TestMessageHandler(TestCase):

    def setUp(self):
        # os.environ.setdefault('MESSAGE_DATABASE_MOCK', 'TRUE')
        self.message_handler = MessagesTagHandler(messages_limit=50)
        self.tags = [{'message_id': 1222, 'is_receipt': False},
                     {'message_id': 2525, 'is_receipt': True}]
        self.messages = [{'id': 2698406951}, {'id': 2698406952},
                         {'id': 2698406953},
                         {'id': 2698406954}, {'id': 2698407037},
                         {'id': 2577499155}, {'id': 2577499203},
                         {'id': 2698406966},
                         {'id': 2698406967}, {'id': 2698407206}]

    def test_load_fifty_messages(self):
        self.message_handler.messages_limit = 50
        messages = self.message_handler.load_messages(offset=1)
        self.assertTrue(len(messages) == 50, msg=messages)

    def test_offset_messages_from_database(self):
        message_offset_one = \
            self.message_handler.load_messages(offset=1)[1]
        message_offset_two = \
            self.message_handler.load_messages(offset=2)[0]
        self.assertEqual(message_offset_one['id'], message_offset_two['id'])

    def test_delete_tags(self):
        tag_ids = [tag['message_id'] for tag in self.tags]
        self.message_handler.delete_tags(tag_ids)

    def test_add_two_answers_and_delete(self):
        tag = self.tags[0]
        tag2 = self.tags[1]
        self.message_handler.add_tags([tag, tag2])
        tags = self.message_handler.get_tags(limit=2)
        self.assertEqual(tags[0]['message_id'], tag['message_id'])
        self.assertEqual(tags[1]['message_id'], tag2['message_id'])
        self.message_handler.delete_tags([tag['message_id'],
                                          tag2['message_id']])

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

    def test_get_next_messages_from_already_tagged_messages(self):
        tagged_messages = self.messages
        next_messages = [msg['id'] for msg in
                         self.message_handler.get_messages_not_in(
                             tagged_messages)]
        zero_messages = [msg_id for msg_id in next_messages
                         if msg_id in tagged_messages]
        self.assertTrue(len(zero_messages) == 0, zero_messages)

    def test_get_next_messages_after_add_messages(self):
        self.message_handler.add_tags(self.tags)
        tag_ids = [tag['message_id'] for tag in self.tags]
        messages = self.message_handler.get_next_messages()
        self.assertTrue(len(messages) > 0)
        for message in messages:
            self.assertNotIn(message['id'], tag_ids)
        self.message_handler.delete_tags(tag_ids)