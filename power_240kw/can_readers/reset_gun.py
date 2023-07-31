import time
import logging

from base_reader import BaseReader
from constants import PECC
from power_240kw.constant_manager_240kw import ConstantManager240KW
from power_240kw.message_helper import Module1Message as mm1, ModuleMessage as mm, Module2Message as mm2

#logger = logging.getLogger(__name__)


class ResetGunModule1(BaseReader):
    arbitration_id = 774

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager240KW()

    def read_input_data(self):
        #logger.info('Reset Gun-1')
        vehicle_status2_g = self._global_data.get_data_status_vehicle2()
        if vehicle_status2_g == 2 or vehicle_status2_g == 13 or vehicle_status2_g == 21 or vehicle_status2_g == 29:
            mm1.digital_output_open_stop1()
            PECC.STATUS1_GUN1_DATA[0] = 0
        else:
            mm1.digital_output_open_stop1()
            time.sleep(5)
            mm.digital_output_open_fan()
            PECC.STATUS1_GUN1_DATA[0] = 0


class ResetGunModule2(BaseReader):
    arbitration_id = 1542

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager240KW()

    def read_input_data(self):
        #logger.info('Reset Gun-2')
        vehicle_status1_g = self._global_data.get_data_status_vehicle1()
        if vehicle_status1_g == 2 or vehicle_status1_g == 13 or vehicle_status1_g == 21 or vehicle_status1_g == 29:
            mm2.digital_output_open_stop2()
            PECC.STATUS1_GUN2_DATA[0] = 0
        else:
            mm2.digital_output_open_stop2()
            time.sleep(5)
            mm.digital_output_open_fan()
            PECC.STATUS1_GUN2_DATA[0] = 0
