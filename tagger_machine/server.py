import os
import tornado.ioloop
import tornado.web

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


class MessageFetchHandler(tornado.web.RequestHandler):

    def get(self):
        pass


def make_app():
    handlers = [
        (r'/static_files/(.*)', tornado.web.StaticFileHandler,
         {'path': CLIENT_STATIC}),
        (r'/', MainHandler),
        (r'/get_messages', MessageFetchHandler),

    ]
    return tornado.web.Application(handlers)


if __name__ == '__main__':
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
