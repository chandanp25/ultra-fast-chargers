from base_reader import BaseReader
from constants_manager import ConstantsManager
from utility import bytetobinary


class DigitalInputReader(BaseReader):
    arbitration_id = 1282

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantsManager()

    def read_input_data(self):
        self._global_data.set_data(bytetobinary(self.data)[0])
