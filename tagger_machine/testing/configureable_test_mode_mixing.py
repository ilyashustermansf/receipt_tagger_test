import ast
import os


class ConfigureableTestModeMixin:
    def __init__(self, env_variable_name=None, is_test_mode=None):
        """
        Mixing to add test mode functionality to objects
        test mode can be enabled explicitly via is_test_mode argument
         or from environment variable

        :param env_variable_name: name of environment variable
        :param is_test_mode:
        """
        self.is_test_mode = False
        if is_test_mode is not None:
            self.is_test_mode = is_test_mode
        elif env_variable_name is not None:
            self.is_test_mode = bool(os.environ.get(
                env_variable_name))

