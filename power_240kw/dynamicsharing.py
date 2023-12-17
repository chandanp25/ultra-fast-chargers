# import the library
import configparser
import time

from power_240kw.factory_reader import FactoryReader, ObjectManager
from caninterface import CanInterface
from persistent_communication import set_status_update

obj_manager = ObjectManager()

def readAllCanData(d):
    reader = FactoryReader.create_reader(d.arbitration_id,d.data, obj_manager)
    if reader:
        reader.read_input_data()


def readFromCan():
    bus = CanInterface.bus_instance
    for m in bus:
        readAllCanData(m)


def perform_action():
    time.sleep(40)
    set_status_update()
    readFromCan()
