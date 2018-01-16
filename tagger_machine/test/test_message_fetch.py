from unittest import TestCase

from tagger_machine.message_fetch import MessageFetch


class TestMessageFetch(TestCase):

    def setUp(self):
        self.message_fetcher = MessageFetch()

