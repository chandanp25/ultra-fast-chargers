import logging
from power_60kw.can_readers import *

logger = logging.getLogger(__name__)


class FactoryReader:

    reader_dict = {
        DigitalInputReader.arbitration_id: DigitalInputReader,
        PowerModule1Reader.arbitration_id: PowerModule1Reader,
        PowerModule2Reader.arbitration_id: PowerModule2Reader,
        Vehicle1StatusReader.arbitration_id: Vehicle1StatusReader,
        Vehicle2StatusReader.arbitration_id: Vehicle2StatusReader
    }

    @staticmethod
    def create_reader(arbitration_id):
        reader_class = FactoryReader.reader_dict.get(arbitration_id)
        if not reader_class:
            logger.warning(f'No matching reader object found for the arbitration ID: {arbitration_id}')
            return None
        return reader_class()
