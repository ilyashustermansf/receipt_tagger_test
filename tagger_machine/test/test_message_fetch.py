from unittest import TestCase, skip

from tagger_machine.message_fetch import MessageFetch


class TestMessageFetch(TestCase):

    def setUp(self):
        self.message_fetcher = MessageFetch()

    def test_load_fifty_messages(self):
        self.assertTrue(len(self.message_fetcher.load_messages(messages_amount=50,
                                                               start=1)) == 50)
    @skip
    def test_add_answers(self):
        pass

    @skip
    def test_load_messages_increased_count(self):
        self.message_fetcher.start += 1
        messages = self.message_fetcher.load_messages(messages_amount=50,
                                                               start=1)
        self.assertEqual(messages[0]['id'], 2)

    @skip
    def test_load_messages_and_commit_answers(self):
        pass

    @skip
    def test_add_and_commit_duplicate_answers(self):
        pass