import requests


def get_url_path(message_id):
    return '{}{}'.format('https://files.superfly.com/files/?msg_id=',
                         message_id)


def main(messages):
    for message in messages:
        message_url = get_url_path(message['id'])
        print(message_url)
        download_save_file(message, message_url)


def download_save_file(message, message_url):
    response = requests.get(message_url)
    html = response.text
    html_file = open('{}.html'.format(message['id']),
                     'w')
    html_file.write(html)
    html_file.close()


if __name__ == '__main__':
    messages = [{'id': 2698406951}, {'id': 2698406952},
                {'id': 2698406953},
                {'id': 2698406954}, {'id': 2698407037},
                {'id': 2577499155}, {'id': 2577499203},
                {'id': 2698406966},
                {'id': 2698406967}, {'id': 2698407206}]
    print('Downloading html messages files...')
    main(messages)
