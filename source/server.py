import json
import logging
import os
import tornado.ioloop
import tornado.web
from tornado.options import parse_command_line, parse_config_file, options, \
    define
from common.persistence_utils import get_message_content
from common.debug_utils import is_dev_environment
from message_tag_handler import MessagesTagHandler

CLIENT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           'web_client'))
CLIENT_STATIC = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             'web_client/static_files'))
if is_dev_environment():
    STORAGE_DIR = 'tests/efs_messages/mnt/efs'
    MESSAGES_STATIC = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   STORAGE_DIR))
else:
    STORAGE_DIR = '/mnt/efs/'
    MESSAGES_STATIC = os.path.abspath(STORAGE_DIR)


class MainHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        with open(CLIENT_PATH + '/index.html', 'r') as file:
            self.write(file.read())


class MessageContentHandler(tornado.web.RequestHandler):

    def get(self, message_id):
        logging.info('Requested message_id={}'.format(message_id))
        self.write(get_message_content(message_id))


class MessageHandler(tornado.web.RequestHandler):

    def initialize(self, message_tag_table):
        self.message_tag_handler = message_tag_table


class MessageFetchHandler(MessageHandler):

    def get(self):
        messages = self.message_tag_handler.get_next_messages()
        self.write(json.dumps(messages))


class AddTagsHandler(MessageHandler):

    def post(self):
        tags = json.loads(self.request.body)
        if isinstance(tags, list) and len(tags) > 0:
            if 'message_id' not in tags[0]:
                return
            self.message_tag_handler.add_tags(tags)

def make_app():
    message_tag_table = dict(message_tag_table=
                             MessagesTagHandler(messages_limit=50))
    handlers = [
        (r'/static_files/(.*)', tornado.web.StaticFileHandler,
         {'path': CLIENT_STATIC}),
        (r'/messages/(.*)', MessageContentHandler),
        (r'/', MainHandler),
        (r'/get_messages', MessageFetchHandler, message_tag_table),
        (r'/add_tags', AddTagsHandler, message_tag_table),
    ]
    return tornado.web.Application(handlers)


if __name__ == '__main__':
    file = open('log.txt', 'w+')
    options.log_file_prefix = 'logs/log.txt'
    parse_command_line()
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
