# import the library
import configparser

from power_240kw.factory_reader import FactoryReader
from caninterface import CanInterface
from persistent_communication import set_status_update

def get_total_power():
    # Create a configparser object
    config = configparser.ConfigParser()
    try:
        # Read the configuration from the INI file
        config.read('config.ini')
        # Access values from sections and keys
        total_power = config.get('total_power', 'TOTAL_POWER')
    except configparser.Error as config_err:
        pass

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
