import logging
from power_60kw.can_readers import *

#logger = logging.getLogger(__name__)


class ObjectManager:
    def __init__(self):
        self._instances = {}

    def get_instance(self, class_name):
        if class_name not in self._instances:
            # If the class is not instantiated, create a new instance
            instance = globals()[class_name]()
            self._instances[class_name] = instance
        return self._instances[class_name]


class FactoryReader:

    reader_dict = {
        DigitalInputReader.arbitration_id: DigitalInputReader,
        PowerModule1Reader.arbitration_id: PowerModule1Reader,
        PowerModule2Reader.arbitration_id: PowerModule2Reader,
        Vehicle1StatusReader.arbitration_id: Vehicle1StatusReader,
        Vehicle2StatusReader.arbitration_id: Vehicle2StatusReader
    }

    @staticmethod
    def create_reader(arbitration_id, data, obj_manager):
        reader_class = FactoryReader.reader_dict.get(arbitration_id)
        if not reader_class:
            # logger.warning(f'No matching reader object found for the arbitration ID: {arbitration_id}')
            return None
        reader_obj = obj_manager.get_instance(reader_class.__name__)
        reader_obj.data = data
        return reader_obj
