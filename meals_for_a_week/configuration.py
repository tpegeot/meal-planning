import logging
import sys


# Configuration class
class Configuration:
    """
    Configuration class
    """
    def __init__(self):
        """
        Init configuration class
        """
        self._debug = False
        self._verbose = False
        self._check_config = False
        self._pretend_only = False
        self._leftover_mode = False
        # Order matters in _meal_type
        self._meal_types = ['VEGGIE', 'SPECIAL', 'NORMAL']
        # Init log
        self._logger = self.init_log()

    def enable_verbose(self):
        """
        Enable verbose mode
        """
        self._verbose = True

    def enable_debug(self):
        """
        Enable debug mode
        """
        self._debug = True

    def enable_check_config(self):
        """
        Enable check config mode only
        """
        self._check_config = True

    def enable_pretend_only(self):
        """
        Enable pretend mode
        """
        self._pretend_only = True

    def enable_leftover_mode(self):
        """
        Enable leftover mode
        """
        self._leftover_mode = True

    def is_verbose(self):
        """
        Return if verbose mode is enable
        :return:
        :rtype:
        """
        return self._verbose

    def is_debug(self):
        """
        Return if debug mode is enable
        :return:
        :rtype:
        """
        return self._debug

    def is_pretend_only(self):
        """
        Return if pretend only mode is enabled
        :return:
        :rtype:
        """
        return self._pretend_only

    def is_leftover_mode(self):
        """
        Return if leftover mode is enabled
        :return:
        :rtype:
        """
        return self._leftover_mode

    def get_meal_types(self):
        """

        :return:
        :rtype:
        """
        return self._meal_types

    # Logging
    @staticmethod
    def init_log():
        """
        Init log mecanism
        :return:
        :rtype:
        """
        __formatter = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s — %(message)s')
        __logger = logging.getLogger('meals_for_a_week')
        __logger.setLevel('WARN')
        __console_handler = logging.StreamHandler(sys.stdout)
        __console_handler.setFormatter(__formatter)
        __logger.addHandler(__console_handler)
        __logger.propagate = False
        return __logger

    def set_debug_log(self):
        """
        Set log level to DEBUG
        """
        self._logger.setLevel('DEBUG')

    def set_verbose_log(self):
        """
        Set log level to INFO
        """
        self._logger.setLevel('INFO')

    def debug_log(self, message):
        """
        Log "message" when log level is DEBUG
        """
        self._logger.debug(message)

    def verbose_log(self, message):
        """
        Log "message" when log level is INFO
        """
        self._logger.info(message)

    def warn_log(self, message):
        """
        Log "message" when log level is WARN
        """
        self._logger.warning(message)

    def error_log(self, message):
        """
        Log "message" when log level is ERROR
        """
        self._logger.error(message)

