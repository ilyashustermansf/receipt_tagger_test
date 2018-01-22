import json
import logging
import os
import tornado.ioloop
import tornado.web

from message_tag_handler import MessagesTagHandler

CLIENT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           'web_client'))
CLIENT_STATIC = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             'web_client/static_files'))
MESSAGES_STATIC = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               'test'))


class MainHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        with open(CLIENT_PATH + '/index.html', 'r') as file:
            self.write(file.read())


class MessageHandler(tornado.web.RequestHandler):

    def initialize(self, message_tag_table):
        self.message_tag_handler = message_tag_table


class MessageFetchHandler(MessageHandler):

    def get(self):
        messages = self.message_tag_handler.get_next_messages_with_content()
        self.write(json.dumps(messages))


class AddTagsHandler(MessageHandler):

    def post(self):
        tags = json.loads(self.request.body)
        if isinstance(tags, list) and len(tags) > 0:
            if 'message_id' not in tags[0]:
                return
            self.message_tag_handler.add_tags(tags)


def make_app():
    logging.basicConfig(format=logging.INFO)
    message_tag_table = dict(message_tag_table=
                             MessagesTagHandler(messages_limit=50))
    handlers = [
        (r'/static_files/(.*)', tornado.web.StaticFileHandler,
         {'path': CLIENT_STATIC}),
        (r'/messages/(.*)', tornado.web.StaticFileHandler,
         {'path': MESSAGES_STATIC}),
        (r'/', MainHandler),
        (r'/get_messages', MessageFetchHandler, message_tag_table),
        (r'/add_tags', AddTagsHandler, message_tag_table),
    ]
    return tornado.web.Application(handlers)


if __name__ == '__main__':
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
