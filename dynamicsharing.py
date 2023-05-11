# import the library
from factory_reader import FactoryReader
from caninterface import CanInterface
from persistent_communication import set_status_update

def readAllCanData(d):
    reader = FactoryReader.create_reader(d.arbitration_id)
    reader.read_input_data()

def readFromCan():
    bus = CanInterface.bus_instance
    for m in bus:
        readAllCanData(m)

def perform_action():
    set_status_update()
    readFromCan()