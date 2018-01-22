import inspect
from os.path import dirname, join
import builtins
from os import environ
import os
import zlib

CALLING_FRAME_INDEX = 2  # location of calling frame in outer frames
CALLING_FUNCTION_INDEX = 1  # location of calling function in frame
FILE_PATH_INDEX = 1  # location of file path in function frame

SQL_DIR = "sql"

SQL_PREFIX = ".sql"

STORAGE_DIR = '/mnt/efs/'
TEST_STORAGE_DIR = '/Users/ilya/PycharmProjects/receipt_tagger/tagger_machine/test/messages/'

TEST_DIRECTORY_ENV = 'TEST_DIRECTORY_ENV'


def get_message_content(message_id):
    message_file_path = _get_message_file_path(message_id)
    with open(message_file_path, 'rb') as file_:
        message_content = file_.read()

    try:
        message_content = zlib.decompress(message_content)
    except zlib.error:
        pass

    decoded_message_content = message_content.decode('utf-8')
    return decoded_message_content


def is_test_mode():
    return bool(os.environ.get(
        TEST_DIRECTORY_ENV) == 'True')


def _get_message_file_path(message_id):
    if is_test_mode():
        return '{}{}.html'.format(TEST_STORAGE_DIR, message_id)

    if not isinstance(message_id, int):
        message_id = int(message_id)

    levels = []

    for i in range(3):  # Create 4 levels
        levels.append(str(message_id % 1000))
        message_id = int(message_id / 1000)

    levels.append(str(message_id))  # The 4th level
    levels.reverse()

    levels_path = '/'.join(levels[:3])
    file_name = "{}.html".format(levels[3])

    message_file_path = os.path.join(STORAGE_DIR, levels_path, file_name)
    return message_file_path


def get_operations_connection_string():
    user_name = get_environment_variable("OPERATIONS_DB_USER_NAME")
    password = get_environment_variable("OPERATIONS_DB_PASSWORD")
    operations_connection_string = "postgresql://{username}:{password}" \
                                   "@operations-db.internal.superfly.com" \
                                   ":5432/operations".format(
        username=user_name, password=password)
    return operations_connection_string


def get_environment_variable(environment_variable_name):
    if environment_variable_name in environ:
        return environ[environment_variable_name]
    else:
        raise SystemError("environment variable: {} - not found".format(
            environment_variable_name))


def get_sql(sql_file_name):
    sql = _get_file(sql_file_name, SQL_PREFIX, SQL_DIR)
    return sql


def _get_file(file_name, file_prefix, file_dir):
    if not file_name.endswith(file_prefix):
        file_name += file_prefix
    file_path = get_file_path(file_name, file_dir,
                              calling_function_increment=2)
    with open(file_path, "r") as f:
        file = f.read()
    return file


def get_file_path(file_name, file_dir, calling_function_increment=0):
    current_frame = inspect.currentframe()
    calling_frame = inspect.getouterframes(current_frame,
                                           CALLING_FRAME_INDEX)
    calling_file_path = \
        calling_frame[CALLING_FUNCTION_INDEX + calling_function_increment][
            FILE_PATH_INDEX]
    calling_directory_name = dirname(calling_file_path)
    file_path = join(calling_directory_name, file_dir, file_name)
    return file_path


def get_calling_file_path(calling_function_increment=0) -> str:
    current_frame = inspect.currentframe()
    calling_frame = inspect.getouterframes(current_frame,
                                           CALLING_FRAME_INDEX)
    calling_file_path = \
        calling_frame[CALLING_FUNCTION_INDEX + calling_function_increment][
            FILE_PATH_INDEX]
    return calling_file_path


def get_striped_lines_from_file(file_path):
    with open(file_path, "r") as file_:
        lines = file_.readlines()
    striped_lines = [line.strip() for line in lines]
    return striped_lines


class utf8_open:
    def __init__(self, path, mode):
        self._file = builtins.open(path, mode, encoding="utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self._file.close()
        self._file = None


if __name__ == '__main__':
    print(get_message_content(2698407037))
