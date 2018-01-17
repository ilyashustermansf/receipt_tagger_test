import os
import tornado.ioloop
import tornado.web

# from flask import Flask, send_from_directory
#
# app = Flask(__name__)
#
#
# # TODO change this to tornado to handle wide requests
# @app.route('/', methods=['GET', 'POST'])
# def main():
#     return send_from_directory('web_client', 'index.html')
#
#
# if __name__ == '__main__':
#     app.run()

VUE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'web_client'))


class MainHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        with open(VUE_PATH + "/index.html", 'r') as file:
            self.write(file.read())


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
