from pytest import fixture
import os
from source.message_tag_handler import MessagesTagHandler

MESSAGES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             'messages'))


def get_html_content(message_id):
    with open('{}/{}.html'.format(MESSAGES_PATH, message_id)) as f:
        return f.read()


@fixture
def message_handler():
    os.environ.setdefault('MESSAGE_DATABASE_MOCK', 'TRUE')
    os.environ.setdefault('TEST_DIRECTORY_ENV', 'True')
    message_handler = MessagesTagHandler(messages_limit=50)
    return message_handler


@fixture
def tags():
    return [{'message_id': 2698406951, 'is_receipt': False},
            {'message_id': 2698406953, 'is_receipt': True}]


@fixture
def messages():
    return [{'id': 2698406951}, {'id': 2698406952},
            {'id': 2698406953},
            {'id': 2698406954}, {'id': 2698407037},
            {'id': 2577499155}, {'id': 2577499203},
            {'id': 2698406966},
            {'id': 2698406967}, {'id': 2698407206}]


@fixture
def html():
    return get_html_content(message_id=2698406951)


def test_load_fifty_messages(message_handler):
    message_handler.messages_limit = 50
    messages = message_handler.load_messages(offset=1)
    assert len(messages) == 50, messages


def test_offset_messages_from_database(message_handler):
    message_offset_one = \
        message_handler.load_messages(offset=1)[1]
    message_offset_two = \
        message_handler.load_messages(offset=2)[0]
    assert message_offset_one['id'] == message_offset_two['id']


def test_delete_tags(message_handler, tags):
    tag_ids = [tag['message_id'] for tag in tags]
    message_handler.delete_tags(tag_ids)


def test_add_two_answers_and_delete(message_handler, tags):
    tag = tags[0]
    tag2 = tags[1]
    message_handler.add_tags([tag, tag2])
    tags_got = message_handler.get_tags(limit=2)
    assert tags_got[0]['message_id'] == tag['message_id']
    assert tags_got[1]['message_id'] == tag2['message_id']
    message_handler.delete_tags([tag['message_id'],
                                 tag2['message_id']])
    tag_got_ids = [tag['message_id'] for tag in tags_got]
    latest_tags = [tag['message_id'] for tag in message_handler.get_tags()]
    for id in tag_got_ids:
        assert id not in latest_tags


def test_get_message_url(message_handler):
    message_id = 1234
    url = message_handler.get_url(message_id)
    assert url == 'https://files.superfly.com/files/?msg_id={}' \
        .format(message_id)


def test_get_messages_urls(message_handler, messages):
    messages_with_urls = message_handler.add_urls(messages)
    for message, message_with_url in zip(messages,
                                         messages_with_urls):
        assert message_with_url['url'] == 'https://files.superfly.com' \
                                          '/files/?msg_id={}' \
            .format(message['id'])
        assert 'id' in message_with_url


def test_get_next_messages_from_already_tagged_messages(message_handler,
                                                        messages):
    tagged_messages = messages
    next_messages = [msg['id'] for msg in
                     message_handler.get_messages_not_in(
                         tagged_messages)]
    zero_messages = [msg_id for msg_id in next_messages
                     if msg_id in tagged_messages]
    assert len(zero_messages) == 0, zero_messages


def test_get_next_messages_after_add_tags(message_handler, tags):
    message_handler.add_tags(tags)
    tag_ids = [tag['message_id'] for tag in tags]
    messages = message_handler.get_next_messages()
    assert len(messages) > 0
    for message in messages:
        assert message['id'] not in tag_ids
    message_handler.delete_tags(tag_ids)


def test_add_tags_that_already_exist(message_handler, tags):
    message_handler.add_tags(tags)
    assert len(message_handler.get_tags()) == 2
    tag_ids = [tag['message_id'] for tag in tags]
    message_handler.add_tags(tags)
    assert len(message_handler.get_tags()) == 2
    message_handler.delete_tags(tag_ids)


def test_html_content(message_handler, html):
    html_content = message_handler.get_html_content(
        message_id=2698406951)
    assert html_content == html


def test_get_messages_contents(message_handler):
    message_handler.messages_limit = 10
    messages_contents = message_handler \
        .get_next_messages_with_content()
    assert len(messages_contents) == 10
    for message in messages_contents:
        assert 'content' in message and 'id' in message
        assert message['content'] == get_html_content(message['id'])
