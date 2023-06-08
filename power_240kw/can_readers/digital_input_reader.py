import logging
from base_reader import BaseReader
from power_240kw.constant_manager_240kw import ConstantManager240KW
from utility import bytetobinary

logger = logging.getLogger(__name__)


class DigitalInputReader(BaseReader):
    arbitration_id = 1282

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager240KW()

    def read_input_data(self):
        logger.info('Reading digital input data for 240KW')
        self._global_data.set_data(bytetobinary(self.data)[0])
