import logging
from power_240kw.can_readers import *

logger = logging.getLogger(__name__)


class FactoryReader:

    reader_dict = {
        DigitalInputReader.arbitration_id: DigitalInputReader,
        PMSetDataCurrentPeccStatus1.arbitration_id: PMSetDataCurrentPeccStatus1,
        PMSetDataCurrentPeccStatus2.arbitration_id: PMSetDataCurrentPeccStatus2,
        PMSetDataCurrentPeccStatus3.arbitration_id: PMSetDataCurrentPeccStatus3,
        PMSetDataCurrentPeccStatus4.arbitration_id: PMSetDataCurrentPeccStatus4,
        PMSetDataCurrentPeccStatus5.arbitration_id: PMSetDataCurrentPeccStatus5,
        PMSetDataCurrentPeccStatus6.arbitration_id: PMSetDataCurrentPeccStatus6,
        Vehicle1StatusReader.arbitration_id: Vehicle1StatusReader,
        Vehicle2StatusReader.arbitration_id: Vehicle2StatusReader,
        ResetGunModule1.arbitration_id: ResetGunModule1,
        ResetGunModule2.arbitration_id: ResetGunModule2
    }

    @staticmethod
    def create_reader(arbitration_id, data):
        reader_class = FactoryReader.reader_dict.get(arbitration_id)
        if not reader_class:
            logger.warning(f'No matching reader object found for the arbitration ID: {arbitration_id}')
            return None
        return reader_class(data)
