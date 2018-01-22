
class MessageTagTableMock(object):

    def __init__(self):
        self.tag_messages = []

    def get_messages_tags(self, limit):
        return self.tag_messages[:limit]

    def insert_tags(self, tags):
        self.tag_messages += tags

    def delete_tags(self, tag_ids):
        self.tag_messages = [tag for tag in self.tag_messages if
                             tag['message_id'] not in tag_ids]

    def get_all_tags(self):
        return self.tag_messages