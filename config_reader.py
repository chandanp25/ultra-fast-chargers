import configparser
from utility import Singleton

POWER_DICT = {
    60: 'power_60kw',
    240: 'power_240kw'
}


class ConfigManager(metaclass=Singleton):
    def __init__(self):
        # Create a configparser object
        self._config = configparser.ConfigParser()
        # Read the configuration from the INI file
        self._config.read('config.ini')
        self._power = None

    def set_power(self, power):
        self._power = POWER_DICT.get(int(power))

    def get_power_config(self, config_param):
        # Access values from sections and keys
        if self._power is None:
            pass    # Todo: Raise custom exception
        result = self._config.get(self._power, config_param)
        return result

    def get_total_power(self):
        total_power_key = 'total_power'
        return self._config.get(total_power_key, 'TOTAL_POWER')
