import json
from unipath import Path


def get_messages_from_file(filename):
    with open(filename, 'r') as f:
        messages = json.load(f)['messages']
        return messages


class MessageTableMock(object):

    def __init__(self):
        filename = Path(Path(__file__).parent, 'messages.json')
        self.messages = get_messages_from_file(filename)

    def get_messages(self, num_messages, offset):
        return self.messages[offset:][:num_messages]

    def get_messages_not_in(self, messages_updated, limit):
        return [message for message in self.messages
                if message['id'] not in messages_updated][:limit]
