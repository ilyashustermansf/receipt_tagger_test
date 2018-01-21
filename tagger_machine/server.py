import json
import logging
import os
import tornado.ioloop
import tornado.web
from tornado_json import schema

from message_tag_handler import MessagesTagHandler

CLIENT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           'web_client'))
CLIENT_STATIC = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             'web_client/static_files'))


class MainHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        # self.set_header('X-Frame-Options', 'ALLOW-FROM https://files.superfly.com/')

    def get(self):
        with open(CLIENT_PATH + '/index.html', 'r') as file:
            self.write(file.read())


class MessageHandler(tornado.web.RequestHandler):

    @classmethod
    def setup(cls):
        logging.basicConfig(level=logging.WARNING)
        logger = logging.getLogger('tagger_machine')
        logger.propagate = False
        logger.setLevel(logging.WARNING)
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        return logger

    def initialize(self, message_tag_table):
        self.message_tag_handler = message_tag_table


class MessageFetchHandler(MessageHandler):

    def get(self):
        # messages = self.message_tag_handler.get_next_messages()
        self.write(json.dumps([{'id': 1234}, {'id': 1235}]))


class AddTagsHandler(MessageHandler):

    def post(self):
        tags = []
        self.message_tag_handler.add_tags(tags)


def make_app():
    MessageHandler.setup()
    message_tag_table = dict(message_tag_table=
                             MessagesTagHandler(messages_limit=50))
    handlers = [
        (r'/static_files/(.*)', tornado.web.StaticFileHandler,
         {'path': CLIENT_STATIC}),
        (r'/', MainHandler),
        (r'/get_messages', MessageFetchHandler, message_tag_table),
        (r'/add_tags', AddTagsHandler, message_tag_table),
    ]
    return tornado.web.Application(handlers)


if __name__ == '__main__':
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
