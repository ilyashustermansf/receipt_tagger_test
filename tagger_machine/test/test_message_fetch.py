from unittest import TestCase, skip

from tagger_machine.message_tag_handler import MessagesTagHandler


class TestMessageFetch(TestCase):

    def setUp(self):
        self.message_handler = MessagesTagHandler()
        self.tags = [{'message_id': 1222, 'is_receipt': False},
                         {'message_id': 2525, 'is_receipt': True}]

    @skip
    def test_load_fifty_messages(self):
        self.assertTrue(len(self.message_handler.
                            load_messages(messages_amount=50,
                                          offset=1)) == 50)
    @skip
    def test_offset_messages_from_database(self):
        dummy_amount = 2
        message_offset_one = \
            self.message_handler.load_messages(messages_amount=dummy_amount,
                                               offset=1)[1]
        message_offset_two = \
            self.message_handler.load_messages(messages_amount=dummy_amount,
                                               offset=2)[0]
        self.assertEqual(message_offset_one['id'], message_offset_two['id'])

    def test_delete_tags(self):
        self.message_handler.delete_tags(self.tags)

    def test_add_two_answers(self):
        tag = self.tags[0]
        tag2 = self.tags[1]
        self.message_handler.add_tags([tag, tag2])
        tags = self.message_handler.get_tags(limit=2)
        self.assertEqual(tags[0]['message_id'], tag['message_id'])
        self.assertEqual(tags[1]['message_id'], tag2['message_id'])
        self.message_handler.delete_tags([tag, tag2])

    @skip
    def test_load_messages_and_commit_answers(self):
        pass

    @skip
    def test_add_and_commit_duplicate_answers(self):
        pass
