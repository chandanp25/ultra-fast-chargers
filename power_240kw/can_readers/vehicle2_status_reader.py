import logging
import time

from base_reader import BaseReader
from constants import PECC, CanId
from power_240kw.constant_manager_240kw import ConstantManager240KW
from power_240kw.message_helper import Module2Message as mm2, ModuleMessage as mm
from utility import bytetobinary, binaryToDecimal, DTH

logger = logging.getLogger(__name__)


class Vehicle2StatusReader(BaseReader):
    arbitration_id = 1537

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager240KW()
        self._binary_data = bytetobinary(data)

    def read_input_data(self):
        logger.info('Read input for Vehicle-2 status')
        vs2 = self._binary_data
        self._global_data.set_data_status_vehicle2(binaryToDecimal(int(vs2[0])))
        vehicle_status2 = binaryToDecimal(int(vs2[0]))
        # print('vhst2',vehicle_status2)
        vehicle_status1_g = self._global_data.get_data_status_vehicle1()
        # print('vhst1',vehicle_status1_g)
        tag_vol2 = binaryToDecimal(int(vs2[2] + vs2[1]))
        target_volatge_from_car2 = int(tag_vol2 / 10)

        tag_curr2 = binaryToDecimal(int(vs2[4] + vs2[3]))
        tag_curr22 = int(tag_curr2 / 10)
        target_current_from_car2 = int(tag_curr22 / 3)
        # Can IDs are inserted in a list and passed to respective helper functions since it is common across this module
        can_id_list = [CanId.CAN_ID_4, CanId.CAN_ID_5, CanId.CAN_ID_6]
        
        if vehicle_status2 == 0:
            mm.digital_output_led_blue()
            mm2.digital_output_ACopen_Gun2()

        if vehicle_status2 == 2:
            mm.digital_output_led_green()
            mm2.digital_output_ACclose_Gun2()
       
        if vehicle_status2 == 13:  # condition and inside loop code change for 240kW
            mm2.digital_output_close_Gun2()
            mm.digital_output_led_green()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            PECC.STATUS1_GUN2_DATA[0] = 1

            cable_check_voltage2 = binaryToDecimal(int(vs2[7] + vs2[6]))

            if cable_check_voltage2 <= 500:
                mm.lowMode_b(can_id_list)
            if cable_check_voltage2 > 500:
                mm.highMode_b(can_id_list)

            mm.setVoltage_b(DTH.convertohex(cable_check_voltage2), can_id_list)
            mm.startModule_b(can_id_list)
            mm.readModule_Voltage_b(can_id_list)

            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm.stopcharging(CanId.STOP_GUN2)
                mm.stopModule_b(can_id_list)
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_stop2()
                time.sleep(5)
                mm.digital_output_open_fan()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[2] == '0' or digitl_input[3] == '1':
                mm.stopcharging(CanId.STOP_GUN2)
                mm.stopModule_b(can_id_list)
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 21:  # condition and inside loop code change for 240kW
            mm2.digital_output_close_Gun2()
            mm.digital_output_led_green()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            if target_volatge_from_car2 <= 500:
                mm.lowMode_b(can_id_list)

            if target_volatge_from_car2 > 500:
                mm.highMode_b(can_id_list)
    
            mm.setVoltage_b(DTH.convertohex(int(target_volatge_from_car2)), can_id_list)        
            mm.setVoltage_b(DTH.convertohex(int(target_volatge_from_car2)), can_id_list) 
            
            RUNNING_CURRENT2 = int(target_current_from_car2)

            self._global_data.set_data_running_current2(RUNNING_CURRENT2)
            mm.setCurrent_b(can_id_list)
            mm.startModule_b(can_id_list)
            mm.readModule_Voltage_b(can_id_list)
            mm.readModule_Current_b(can_id_list)
            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm.stopcharging(CanId.STOP_GUN2)
                mm.stopModule_b(can_id_list)
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_stop2()
                time.sleep(5)
                mm.digital_output_open_fan()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[2] == '0' or digitl_input[3] == '1':
                mm.stopcharging(CanId.STOP_GUN2)
                mm.stopModule_b(can_id_list)
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 29:  # condition and inside loop code change for 240kW
            mm2.digital_output_close_Gun2()
            mm.digital_output_led_green()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))

            if target_volatge_from_car2 <= 500:
                mm.lowMode_b(can_id_list)

            if target_volatge_from_car2 > 500:
                mm.highMode_b(can_id_list)

            mm.setVoltage_b(DTH.convertohex(int(target_volatge_from_car2)), can_id_list)
            RUNNING_CURRENT2 = int(target_current_from_car2)
            self._global_data.set_data_running_current2(RUNNING_CURRENT2)

            mm.setCurrent_b(can_id_list)
            mm.startModule_b(can_id_list)
            mm.readModule_Voltage_b(can_id_list)
            mm.readModule_Current_b(can_id_list)
            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm.stopcharging(CanId.STOP_GUN2)
                mm.stopModule_b(can_id_list)
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_stop2()
                time.sleep(5)
                mm.digital_output_open_fan()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[2] == '0' or digitl_input[3] == '1':
                mm.stopcharging(CanId.STOP_GUN2)
                mm.stopModule_b(can_id_list)
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 37 or vehicle_status2 == 35:  # condition and inside loop code change for 240kW
            mm.stopModule_b(can_id_list)
            mm.digital_output_led_red()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            mm.readModule_Voltage_b(can_id_list)
            mm.readModule_Current_b(can_id_list)
            PECC.STATUS1_GUN2_DATA[0] = 1
