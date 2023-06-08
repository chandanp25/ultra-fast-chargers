import can
from caninterface import CanInterface
from power_240kw.constant_manager_240kw import ConstantManager240KW
from constants import CanId
from utility import DTH


class ModuleMessage:
    bus = CanInterface.bus_instance

    @classmethod
    def digital_output_open_fan(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[0, 0, 16, 0])  # data changed for 240kW
        cls.bus.send(message)

    @classmethod
    def stopcharging(cls, can_id):
        message = can.Message(arbitration_id=can_id, is_extended_id=False, data=[])
        cls.bus.send(message)

    @classmethod
    def lowMode_a(cls, can_ids):
        if not isinstance(can_ids, list):
            can_ids = [can_ids]
        for can_id in can_ids:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
                16, 95, 0, 0, 0, 0, 0, 2])
            cls.bus.send(message)

    @classmethod
    def lowMode_b(cls, can_ids):
        if not isinstance(can_ids, list):
            can_ids = [can_ids]
        for can_id in can_ids:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            32, 95, 0, 0, 0, 0, 0, 2])
            cls.bus.send(message)

    @classmethod
    def highMode_a(cls, can_ids):
        if not isinstance(can_ids, list):
            can_ids = [can_ids]
        for can_id in can_ids:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            16, 95, 0, 0, 0, 0, 0, 1])
            cls.bus.send(message)

    @classmethod
    def highMode_b(cls, can_ids):
        if not isinstance(can_ids, list):
            can_ids = [can_ids]
        for can_id in can_ids:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            32, 95, 0, 0, 0, 0, 0, 1])
            cls.bus.send(message)

    @classmethod
    def stopModule_a(cls, can_ids):
        if not isinstance(can_ids, list):
            can_ids = [can_ids]
        for can_id in can_ids:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            16, 4, 0, 0, 0, 0, 0, 1])
            cls.bus.send(message)

    @classmethod
    def stopModule_b(cls, can_ids):
        if not isinstance(can_ids, list):
            can_ids = [can_ids]
        for can_id in can_ids:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            32, 4, 0, 0, 0, 0, 0, 1])
            cls.bus.send(message)

    @classmethod
    def setVoltage_a(cls, voltageValue, can_ids):
        if not isinstance(can_ids, list):
            can_ids = [can_ids]
        for can_id in can_ids:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[16, 2, 0, 0, 0] + voltageValue)
            cls.bus.send(message)

    @classmethod
    def setVoltage_b(cls, voltageValue, can_ids):
        if not isinstance(can_ids, list):
            can_ids = [can_ids]
        for can_id in can_ids:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[32, 2, 0, 0, 0] + voltageValue)
            cls.bus.send(message)

    @classmethod
    def setCurrent_a(cls, can_ids):
        global_data = ConstantManager240KW()
        tmp_current1 = DTH.convertohex(global_data.get_data_running_current1())

        if not isinstance(can_ids, list):
            can_ids = [can_ids]
        for can_id in can_ids:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[16, 3, 0, 0, 0] + tmp_current1)
            cls.bus.send(message)

    @classmethod
    def setCurrent_b(cls, can_ids):
        global_data = ConstantManager240KW()
        tmp_current1 = DTH.convertohex(global_data.get_data_running_current1())

        if not isinstance(can_ids, list):
            can_ids = [can_ids]
        for can_id in can_ids:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[32, 3, 0, 0, 0] + tmp_current1)
            cls.bus.send(message)

    @classmethod
    def startModule_a(cls, can_ids):
        if not isinstance(can_ids, list):
            can_ids = [can_ids]
        for can_id in can_ids:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            16, 4, 0, 0, 0, 0, 0, 0])
            cls.bus.send(message)

    @classmethod
    def startModule_b(cls, can_ids):
        if not isinstance(can_ids, list):
            can_ids = [can_ids]
        for can_id in can_ids:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            32, 4, 0, 0, 0, 0, 0, 0])
            cls.bus.send(message)

    @classmethod
    def readModule_Voltage_a(cls, can_ids):
        if not isinstance(can_ids, list):
            can_ids = [can_ids]
        for can_id in can_ids:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            18, 98, 0, 0, 0, 0, 0, 0])
            cls.bus.send(message)

    @classmethod
    def readModule_Voltage_b(cls, can_ids):
        if not isinstance(can_ids, list):
            can_ids = [can_ids]
        for can_id in can_ids:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            34, 98, 0, 0, 0, 0, 0, 0])
            cls.bus.send(message)

    @classmethod
    def readModule_Current_a(cls, can_id):
        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            18, 48, 0, 0, 0, 0, 0, 0])
        cls.bus.send(message)

    @classmethod
    def readModule_Current_b(cls, can_id):
        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            34, 48, 0, 0, 0, 0, 0, 0])
        cls.bus.send(message)

    @classmethod
    def pecc_powers_voltage_limits(cls, can_id):
        message = can.Message(arbitration_id=can_id,
                              is_extended_id=False, data=[220, 5, 16, 39, 224, 46, 0, 0])
        cls.bus.send(message)

    @classmethod
    def pecc_current_limits(cls, can_id):
        message = can.Message(arbitration_id=can_id,
                              is_extended_id=False, data=[0, 0, 196, 9])
        cls.bus.send(message)


class Module1Message(ModuleMessage):

    @classmethod
    def digital_output_close_Gun1(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[51, 0, 255, 0])  # data changed for 240kW
        cls.bus.send(message)

    @classmethod
    def digital_output_open_stop1(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[0, 0, 35, 0])  # data changed for 240kW
        cls.bus.send(message)

    @classmethod
    def pecc_status_1_Gun1(cls):
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_GUN1,
                              is_extended_id=False, data=[0, 0, 0, 0, 0, 0, 0])
        cls.bus.send(message)

    def pecc_status_2_Gun1(cls):
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_GUN1,
                              is_extended_id=False, data=[0, 0, 0, 0, 0, 0, 0])
        cls.bus.send(message)


class Module2Message(ModuleMessage):

    @classmethod
    def digital_output_close_Gun2(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[92, 0, 255, 0])  # data changed for 240kW
        cls.bus.send(message)

    @classmethod
    def digital_output_open_stop2(cls):
        message = can.Message(arbitration_id=CanId.DIGITAL_OUT,
                              is_extended_id=False, data=[0, 0, 76, 0])  # data changed for 240kW
        cls.bus.send(message)

    @classmethod
    def pecc_status_1_Gun2(cls):
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_Gun2,
                              is_extended_id=False, data=[0, 0, 0, 0, 0, 0, 0])
        cls.bus.send(message)

    def pecc_status_2_Gun2(cls):
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_Gun2,
                              is_extended_id=False, data=[0, 0, 0, 0, 0, 0, 0])
        cls.bus.send(message)
