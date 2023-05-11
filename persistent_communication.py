import can
import threading
import time

from constants import PECC, CanId
from caninterface import CanInterface

class SetInterval:
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        try:
            thread=threading.Thread(target=self.__setInterval)
            thread.start()
        except threading.ThreadException as err:
            pass

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()


class PECCStatusManager:
    # Bus interface
    bus = CanInterface.bus_instance

    @staticmethod
    def pecc_powers_voltage_limits_1():
        message = can.Message(arbitration_id=CanId.PECC_POWER_VOLTAGE_L1,
                              is_extended_id=False, data=PECC.LIMITS1_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_current_limits_1():
        message = can.Message(arbitration_id=CanId.PECC_CURRENT_L1,
                              is_extended_id=False, data=PECC.LIMITS2_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_1_Gun1():
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_GUN1,
                              is_extended_id=False, data=PECC.STATUS1_GUN1_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_2_Gun1():
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_GUN1,
                              is_extended_id=False, data=PECC.STATUS2_GUN1_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_powers_voltage_limits_2():
        message = can.Message(arbitration_id=CanId.PECC_POWER_VOLTAGE_L2,
                              is_extended_id=False, data=PECC.LIMITS1_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_current_limits_2():
        message = can.Message(arbitration_id=CanId.PECC_CURRENT_L2,
                              is_extended_id=False, data=PECC.LIMITS2_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_1_Gun2():
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_Gun2,
                              is_extended_id=False, data=PECC.STATUS1_GUN2_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_2_Gun2():
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_Gun2,
                              is_extended_id=False, data=PECC.STATUS2_GUN2_DATA)
        PECCStatusManager.bus.send(message)


def set_status_update():
    # Get all the attributes of the class
    attributes = dir(PECCStatusManager)

    # Filter for methods
    send_status_methods = [attr for attr in attributes if callable(getattr(PECCStatusManager, attr))]

    # Invoke all the methods
    for send_status in send_status_methods:
        send_status_method = getattr(PECCStatusManager, send_status)
        SetInterval(0.25, send_status_method)
