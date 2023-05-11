import can
from caninterface import CanInterface
from constants_manager import ConstantsManager
from constants import CanId
from utility import DTH


class ModuleMessage:
    bus = CanInterface.bus_instance

    @classmethod
    def digital_output_open_fan(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[0, 0, 243, 0])
        cls.bus.send(message)


class Module1Message(ModuleMessage):

    @classmethod
    def digital_output_close_Gun1(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[243, 0, 255, 0])
        cls.bus.send(message)

    @classmethod
    def digital_output_load1(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[204, 0, 252, 0])
        cls.bus.send(message)

    @classmethod
    def digital_output_Gun1_load2(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[195, 0, 243, 0])
        cls.bus.send(message)

    @classmethod
    def lowMode1(cls):
        message = can.Message(arbitration_id=CanId.CAN_ID_1, is_extended_id=True, data=[
            16, 95, 0, 0, 0, 0, 0, 2])
        cls.bus.send(message)

    @classmethod
    def highMode1(cls):
        message = can.Message(arbitration_id=CanId.CAN_ID_1, is_extended_id=True, data=[
            16, 95, 0, 0, 0, 0, 0, 1])
        cls.bus.send(message)

    @classmethod
    def digital_output_open_stop1(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[0, 0, 191, 0])
        cls.bus.send(message)

    @classmethod
    def digital_output_open_load1(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[0, 0, 51, 0])
        cls.bus.send(message)

    @classmethod
    def readModule_Voltage_1(cls):
        message = can.Message(arbitration_id=CanId.CAN_ID_1, is_extended_id=True, data=[
            18, 98, 0, 0, 0, 0, 0, 0])
        cls.bus.send(message)

    @classmethod
    def readModule_Current_1(cls):
        message = can.Message(arbitration_id=CanId.CAN_ID_1, is_extended_id=True, data=[
            18, 48, 0, 0, 0, 0, 0, 0])
        cls.bus.send(message)

    @classmethod
    def stopcharging1(cls):
        message = can.Message(arbitration_id=CanId.STOP_GUN1, is_extended_id=False, data=[])
        cls.bus.send(message)

    @classmethod
    def stopModule1(cls):
        message = can.Message(arbitration_id=CanId.CAN_ID_1, is_extended_id=True, data=[
            16, 4, 0, 0, 0, 0, 0, 1])
        cls.bus.send(message)

    @classmethod
    def setVoltage1(cls, voltageValue):
        message = can.Message(arbitration_id=CanId.CAN_ID_1, is_extended_id=True, data=[16, 2, 0, 0, 0] + voltageValue)
        cls.bus.send(message)

    @classmethod
    def setCurrent1(cls):
        global_data = ConstantsManager()
        tmp_current = DTH.convertohex(global_data.get_data_running_current())
        message = can.Message(arbitration_id=CanId.CAN_ID_1, is_extended_id=True, data=[16, 3, 0, 0, 0] + tmp_current)
        cls.bus.send(message)

    @classmethod
    def startModule1(cls):
        message = can.Message(arbitration_id=CanId.CAN_ID_1, is_extended_id=True, data=[
            16, 4, 0, 0, 0, 0, 0, 0])
        cls.bus.send(message)


class Module2Message(ModuleMessage):

    @classmethod
    def digital_output_close_Gun2(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[252, 0, 255, 0])
        cls.bus.send(message)

    @classmethod
    def digital_output_load2(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[195, 0, 243, 0])
        cls.bus.send(message)

    @classmethod
    def digital_output_Gun2_load1(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[204, 0, 252, 0])
        cls.bus.send(message)

    @classmethod
    def lowMode2(cls):
        message = can.Message(arbitration_id=CanId.CAN_ID_2, is_extended_id=True, data=[
            16, 95, 0, 0, 0, 0, 0, 2])
        cls.bus.send(message)

    @classmethod
    def highMode2(cls):
        message = can.Message(arbitration_id=CanId.CAN_ID_2, is_extended_id=True, data=[
            16, 95, 0, 0, 0, 0, 0, 1])
        cls.bus.send(message)

    @classmethod
    def digital_output_open_stop2(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[0, 0, 191, 0])
        cls.bus.send(message)

    @classmethod
    def digital_output_open_load2(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[0, 0, 60, 0])
        cls.bus.send(message)

    @classmethod
    def readModule_Voltage_2(cls):
        message = can.Message(arbitration_id=CanId.CAN_ID_2, is_extended_id=True, data=[
            18, 98, 0, 0, 0, 0, 0, 0])
        cls.bus.send(message)

    @classmethod
    def readModule_Current_2(cls):
        message = can.Message(arbitration_id=CanId.CAN_ID_2, is_extended_id=True, data=[
            18, 48, 0, 0, 0, 0, 0, 0])
        cls.bus.send(message)

    @classmethod
    def stopcharging2(cls):
        message = can.Message(arbitration_id=CanId.STOP_GUN2, is_extended_id=False, data=[])
        cls.bus.send(message)

    @classmethod
    def stopModule2(cls):
        message = can.Message(arbitration_id=CanId.CAN_ID_2, is_extended_id=True, data=[
            16, 4, 0, 0, 0, 0, 0, 1])
        cls.bus.send(message)

    @classmethod
    def setVoltage2(cls, voltageValue):
        message = can.Message(arbitration_id=CanId.CAN_ID_2, is_extended_id=True, data=[16, 2, 0, 0, 0] + voltageValue)
        cls.bus.send(message)

    @classmethod
    def setCurrent2(cls):
        global_data = ConstantsManager()
        tmp_current1 = DTH.convertohex(global_data.get_data_running_current())
        message = can.Message(arbitration_id=CanId.CAN_ID_2, is_extended_id=True, data=[16, 3, 0, 0, 0] + tmp_current1)

        cls.bus.send(message)

    @classmethod
    def startModule2(cls):
        message = can.Message(arbitration_id=CanId.CAN_ID_2, is_extended_id=True, data=[
            16, 4, 0, 0, 0, 0, 0, 0])
        cls.bus.send(message)
