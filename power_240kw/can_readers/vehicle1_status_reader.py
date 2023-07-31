import logging
import time

from base_reader import BaseReader
from constants import PECC, CanId
from power_240kw.constant_manager_240kw import ConstantManager240KW
from power_240kw.message_helper import Module1Message as mm1, ModuleMessage as mm
from utility import bytetobinary, binaryToDecimal, DTH

logger = logging.getLogger(__name__)


class Vehicle1StatusReader(BaseReader):
    arbitration_id = 769

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager240KW()
        self._binary_data = bytetobinary(data)

    def read_input_data(self):
        logger.info('Read input for Vehicle-1 status')
        vs1 = self._binary_data
        self._global_data.set_data_status_vehicle1(binaryToDecimal(int(vs1[0])))
        vehicle_status1 = binaryToDecimal(int(vs1[0]))
        # print('vhst1',vehicle_status1)
        vehicle_status2_g = self._global_data.get_data_status_vehicle2()
        # print('vhst2',vehicle_status2_g)
        tag_vol1 = binaryToDecimal(int(vs1[2] + vs1[1]))
        target_volatge_from_car1 = int(tag_vol1 / 10)

        tag_curr1 = binaryToDecimal(int(vs1[4] + vs1[3]))
        tag_curr11 = int(tag_curr1 / 10)
        target_current_from_car1 = int(tag_curr11 / 3)
        # Can IDs are inserted in a list and passed to respective helper functions since it is common across this module
        can_id_list = [CanId.CAN_ID_1, CanId.CAN_ID_2, CanId.CAN_ID_3]
        if vehicle_status1 == 0 : 
            mm.digital_output_led_blue()
            mm1.digital_output_ACopen_Gun1()

        if vehicle_status1 == 2:
            mm.digital_output_led_green()
            mm1.digital_output_ACclose_Gun1()
        
        if vehicle_status1 == 13:  # condition and inside loop code change for 240kW
            mm1.digital_output_close_Gun1()
            mm.digital_output_led_green()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1

            cable_check_voltage1 = binaryToDecimal(int(vs1[7] + vs1[6]))

            if cable_check_voltage1 <= 500:
                mm.lowMode_a(can_id_list)
            if cable_check_voltage1 > 500:
                mm.highMode_a(can_id_list)

            mm.setVoltage_a(DTH.convertohex(cable_check_voltage1), can_id_list)
            mm.startModule_a(can_id_list)
            mm.readModule_Voltage_a(can_id_list)

            digitl_input = self._global_data.get_data()
            if digitl_input[4] == '1':
                mm.stopcharging(CanId.STOP_GUN1)
                mm.stopModule_a(can_id_list)
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_stop1()
                time.sleep(5)
                mm.digital_output_open_fan()

            if digitl_input[4] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[2] == '0' or digitl_input[3] == '1':
                mm.stopcharging(CanId.STOP_GUN1)
                mm.stopModule_a(can_id_list)
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 21:  # condition and inside loop code change for 240kW
            mm1.digital_output_close_Gun1()
            mm.digital_output_led_green()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            if target_volatge_from_car1 <= 500:
                mm.lowMode_a(can_id_list)

            if target_volatge_from_car1 > 500:
                mm.highMode_a(can_id_list)

            mm.setVoltage_a(DTH.convertohex(int(target_volatge_from_car1)), can_id_list)

            RUNNING_CURRENT1 = int(target_current_from_car1)

            self._global_data.set_data_running_current1(RUNNING_CURRENT1)
            mm.setCurrent_a(can_id_list)
            mm.startModule_a(can_id_list)
            mm.readModule_Voltage_a(can_id_list)
            mm.readModule_Current_a(can_id_list)
            digital_input = self._global_data.get_data()
            if digital_input[4] == '1':
                mm.stopcharging(CanId.STOP_GUN1)
                mm.stopModule_a(can_id_list)
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_stop1()
                time.sleep(5)
                mm.digital_output_open_fan()

            if digital_input[4] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digital_input[2] == '0' or digital_input[3] == '1':
                mm.stopcharging(CanId.STOP_GUN1)
                mm.stopModule_a(can_id_list)
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 29:  # condition and inside loop code change for 240kW
            mm1.digital_output_close_Gun1()
            mm.digital_output_led_green()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))

            if target_volatge_from_car1 <= 500:
                mm.lowMode_a(can_id_list)

            if target_volatge_from_car1 > 500:
                mm.highMode_a(can_id_list)

            mm.setVoltage_a(DTH.convertohex(int(target_volatge_from_car1)), can_id_list)

            RUNNING_CURRENT1 = int(target_current_from_car1)
            self._global_data.set_data_running_current1(RUNNING_CURRENT1)

            mm.setCurrent_a(can_id_list)
            mm.startModule_a(can_id_list)
            mm.readModule_Voltage_a(can_id_list)
            mm.readModule_Current_a(can_id_list)
            digitl_input = self._global_data.get_data()
            if digitl_input[4] == '1':
                mm.stopcharging(CanId.STOP_GUN1)
                mm.stopModule_a(can_id_list)
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_stop1()
                time.sleep(5)
                mm.digital_output_open_fan()

            if digitl_input[4] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[2] == '0' or digitl_input[3] == '1':
                mm.stopcharging(CanId.STOP_GUN1)
                mm.stopModule_a(can_id_list)
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 37 or vehicle_status1 == 35:  # condition and inside loop code change for 240kW
            mm.stopModule_a(can_id_list)
            mm.digital_output_led_red()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            mm.readModule_Voltage_a(can_id_list)
            mm.readModule_Current_a(can_id_list)
            PECC.STATUS1_GUN1_DATA[0] = 1
