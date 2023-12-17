# import the library
import configparser

from power_60kw.factory_reader import FactoryReader, ObjectManager
from caninterface import CanInterface
from persistent_communication import set_status_update

obj_manager = ObjectManager()


def readAllCanData(d):
    reader = FactoryReader.create_reader(d.arbitration_id, d.data, obj_manager)
    if reader:
        reader.read_input_data()


def readFromCan():
    bus = CanInterface.bus_instance
    for m in bus:
        readAllCanData(m)


def perform_action():
    set_status_update()
    readFromCan()
