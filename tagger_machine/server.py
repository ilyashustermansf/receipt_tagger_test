from flask import Flask, send_from_directory

app = Flask(__name__)


# TODO change this to tornado to handle wide requests
@app.route('/', methods=['GET', 'POST'])
def main():
    return send_from_directory('web_client', 'index.html')


if __name__ == '__main__':
    app.run()
