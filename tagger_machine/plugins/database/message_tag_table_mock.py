import json
from unipath import Path


def get_messages_from_file(filename):
    with open(filename, 'r') as f:
        tag_messages = json.load(f)['tag_messages']
        return tag_messages


class MessageTagTableMock(object):

    def __init__(self):
        filename = Path(Path(__file__).parent, 'tag_messages.json')
        self.tag_messages = get_messages_from_file(filename)

    def get_messages_tags(self, limit=5):
        return self.tag_messages[:limit]

    def insert_tags(self, tags):
        self.tag_messages += tags

    def delete_tags(self, tags):
        tag_ids = [tag['message_id'] for tag in tags]
        self.tag_messages = [tag for tag in self.tag_messages if
                             tag['message_id'] not in tag_ids]
