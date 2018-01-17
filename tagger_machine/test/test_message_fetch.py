from unittest import TestCase, skip

from tagger_machine.message_fetch import MessagesHandler


class TestMessageFetch(TestCase):

    def setUp(self):
        self.message_fetcher = MessagesHandler()

    def test_load_fifty_messages(self):
        self.assertTrue(len(self.message_fetcher.
                            load_messages(messages_amount=50,
                                          offset=1)) == 50)

    def test_offset_messages_from_database(self):
        dummy_amount = 2
        message_offset_one = \
            self.message_fetcher.load_messages(messages_amount=dummy_amount,
                                               offset=1)[1]
        message_offset_two = \
            self.message_fetcher.load_messages(messages_amount=dummy_amount,
                                               offset=2)[0]
        self.assertEqual(message_offset_one['id'], message_offset_two['id'])

    @skip
    def test_add_answers(self):
        #TODO
        pass

    @skip
    def test_load_messages_and_commit_answers(self):
        pass

    @skip
    def test_add_and_commit_duplicate_answers(self):
        pass
