import logging
import time

from base_reader import BaseReader
from constants import PECC, CanId
from power_60kw.constant_manager_60kw import ConstantManager60KW
from power_60kw.message_helper import Module1Message as mm1, ModuleMessage as mm
from utility import bytetobinary, binaryToDecimal, DTH

#logger = logging.getLogger(__name__)


class Vehicle1StatusReader(BaseReader):
    arbitration_id = 769

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager60KW()
        self._binary_data = bytetobinary(data)

    def read_input_data(self):
        #logger.info('Read input for Vehicle-1 status')
        vs1 = self._binary_data
        self._global_data.set_data_status_vehicle1(binaryToDecimal(int(vs1[0])))
        vehicle_status1 = binaryToDecimal(int(vs1[0]))
        #logger.info(f'Vehicle-1 status {vehicle_status1}')
        vehicle_status2_g = self._global_data.get_data_status_vehicle2()
        #logger.info(f'Vehicle-2 status {vehicle_status2_g}')
        tag_vol1 = binaryToDecimal(int(vs1[2] + vs1[1]))
        target_volatge_from_car1 = int(tag_vol1 / 10)

        tag_curr1 = binaryToDecimal(int(vs1[4] + vs1[3]))
        tag_curr11 = int(tag_curr1 / 10)
        target_current_from_car1 = int(tag_curr11 / 2)

        if vehicle_status1 == 2 and vehicle_status2_g == 2:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0

        if vehicle_status1 == 13 and vehicle_status2_g == 0 or vehicle_status1 == 13 and vehicle_status2_g == 6:
            PECC.LIMITS1_DATA[4] = 120
            PECC.LIMITS1_DATA[5] = 5
            PECC.LIMITS2_DATA[2] = 44
            PECC.LIMITS2_DATA[3] = 1
            mm1.digital_output_close_Gun1()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1

            cable_check_voltage1 = binaryToDecimal(int(vs1[7] + vs1[6]))

            if cable_check_voltage1 <= 500:
                mm.lowMode(CanId.CAN_ID_1)
                mm.lowMode(CanId.CAN_ID_2)
            if cable_check_voltage1 > 500:
                mm.highMode(CanId.CAN_ID_1)
                mm.highMode(CanId.CAN_ID_2)

            mm.setVoltage(DTH.convertohex(cable_check_voltage1), CanId.CAN_ID_1)
            mm.setVoltage(DTH.convertohex(cable_check_voltage1), CanId.CAN_ID_2)
            mm.startModule(CanId.CAN_ID_1)
            mm.startModule(CanId.CAN_ID_2)
            mm.readModule_Voltage(CanId.CAN_ID_1)

            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm.digital_output_open_stop(CanId.CAN_ID_1)
                time.sleep(5)
                mm.digital_output_open_fan()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 13 and vehicle_status2_g == 2 or vehicle_status1 == 13 and vehicle_status2_g == 37 or vehicle_status1 == 13 and vehicle_status2_g == 35:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm.stopModule(CanId.CAN_ID_2)
            mm1.digital_output_Gun1_load2()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1

            cable_check_voltage1 = binaryToDecimal(int(vs1[7] + vs1[6]))

            if cable_check_voltage1 <= 500:
                mm.lowMode(CanId.CAN_ID_1)

            if cable_check_voltage1 > 500:
                mm.highMode(CanId.CAN_ID_1)

            mm.setVoltage(DTH.convertohex(cable_check_voltage1), CanId.CAN_ID_1)
            mm.stopModule(CanId.CAN_ID_1)
            mm.readModule_Voltage(CanId.CAN_ID_1)

            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)

                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_load1()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 13 and vehicle_status2_g == 13 or vehicle_status1 == 13 and vehicle_status2_g == 21 or vehicle_status1 == 13 and vehicle_status2_g == 29:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm1.digital_output_load1()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1

            cable_check_voltage1 = binaryToDecimal(int(vs1[7] + vs1[6]))

            if cable_check_voltage1 <= 500:
                mm.lowMode(CanId.CAN_ID_1)

            if cable_check_voltage1 > 500:
                mm.highMode(CanId.CAN_ID_1)

            mm.setVoltage(DTH.convertohex(cable_check_voltage1), CanId.CAN_ID_1)
            mm.startModule(CanId.CAN_ID_1)

            mm.readModule_Voltage(CanId.CAN_ID_1)

            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_load1()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 21 and vehicle_status2_g == 0 or vehicle_status1 == 21 and vehicle_status2_g == 6:
            PECC.LIMITS1_DATA[4] = 120
            PECC.LIMITS1_DATA[5] = 5
            PECC.LIMITS2_DATA[2] = 44
            PECC.LIMITS2_DATA[3] = 1
            mm1.digital_output_close_Gun1()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1
            if target_volatge_from_car1 <= 500:
                mm.lowMode(CanId.CAN_ID_2)

            if target_volatge_from_car1 > 500:
                mm.highMode(CanId.CAN_ID_2)

            mm.setVoltage(DTH.convertohex(int(target_volatge_from_car1)), CanId.CAN_ID_1)
            mm.setVoltage(DTH.convertohex(int(target_volatge_from_car1)), CanId.CAN_ID_2)
            RUNNING_CURRENT = int(target_current_from_car1)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm.setCurrent(CanId.CAN_ID_1)
            mm.setCurrent(CanId.CAN_ID_2)
            mm.startModule(CanId.CAN_ID_1)
            mm.startModule(CanId.CAN_ID_2)
            mm.readModule_Voltage(CanId.CAN_ID_1)
            mm.readModule_Current(CanId.CAN_ID_1)
            mm.readModule_Current(CanId.CAN_ID_2)
            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm.digital_output_open_stop(CanId.CAN_ID_1)
                time.sleep(5)
                mm1.digital_output_open_fan()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 21 and vehicle_status2_g == 2 or vehicle_status1 == 21 and vehicle_status2_g == 35 or vehicle_status1 == 21 and vehicle_status2_g == 37:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm.stopModule(CanId.CAN_ID_2)
            mm1.digital_output_Gun1_load2()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1

            mm.setVoltage(DTH.convertohex(target_volatge_from_car1), CanId.CAN_ID_1)

            RUNNING_CURRENT = int(target_current_from_car1 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm.setCurrent(CanId.CAN_ID_1)
            mm.startModule(CanId.CAN_ID_1)
            mm.readModule_Voltage(CanId.CAN_ID_1)
            mm.readModule_Current(CanId.CAN_ID_1)
            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_load1()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 21 and vehicle_status2_g == 13 or vehicle_status1 == 21 and vehicle_status2_g == 21 or vehicle_status1 == 21 and vehicle_status2_g == 29:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm1.digital_output_load1()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1

            mm.setVoltage(DTH.convertohex(target_volatge_from_car1), CanId.CAN_ID_1)

            RUNNING_CURRENT = int(target_current_from_car1 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm.setCurrent(CanId.CAN_ID_1)
            mm.startModule(CanId.CAN_ID_1)
            mm.readModule_Voltage(CanId.CAN_ID_1)
            mm.readModule_Current(CanId.CAN_ID_1)
            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_load1()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 29 and vehicle_status2_g == 0 or vehicle_status1 == 29 and vehicle_status2_g == 6:
            PECC.LIMITS1_DATA[4] = 120
            PECC.LIMITS1_DATA[5] = 5
            PECC.LIMITS2_DATA[2] = 44
            PECC.LIMITS2_DATA[3] = 1
            mm1.digital_output_close_Gun1()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1
            if target_volatge_from_car1 <= 500:
                mm.lowMode(CanId.CAN_ID_2)

            if target_volatge_from_car1 > 500:
                mm.highMode(CanId.CAN_ID_2)

            mm.setVoltage(DTH.convertohex(target_volatge_from_car1), CanId.CAN_ID_1)
            mm.setVoltage(DTH.convertohex(int(target_volatge_from_car1)), CanId.CAN_ID_2)

            RUNNING_CURRENT = int(target_current_from_car1)
            self._global_data.set_data_running_current(RUNNING_CURRENT)

            mm.setCurrent(CanId.CAN_ID_1)
            mm.setCurrent(CanId.CAN_ID_2)
            mm.startModule(CanId.CAN_ID_1)
            mm.stopModule(CanId.CAN_ID_2)
            mm.readModule_Voltage(CanId.CAN_ID_1)
            mm.readModule_Current(CanId.CAN_ID_1)
            mm.readModule_Current(CanId.CAN_ID_2)
            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm.digital_output_open_stop(CanId.CAN_ID_1)
                time.sleep(5)
                mm1.digital_output_open_fan()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 29 and vehicle_status2_g == 2 or vehicle_status1 == 29 and vehicle_status2_g == 35 or vehicle_status1 == 29 and vehicle_status2_g == 37:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm1.digital_output_Gun1_load2()
            mm.stopModule(CanId.CAN_ID_2)
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))

            mm.setVoltage(DTH.convertohex(target_volatge_from_car1), CanId.CAN_ID_1)

            RUNNING_CURRENT = int(target_current_from_car1 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm.setCurrent(CanId.CAN_ID_1)
            mm.startModule(CanId.CAN_ID_1)
            mm.readModule_Voltage(CanId.CAN_ID_1)
            mm.readModule_Current(CanId.CAN_ID_1)
            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_load1()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 29 and vehicle_status2_g == 13 or vehicle_status1 == 29 and vehicle_status2_g == 21 or vehicle_status1 == 29 and vehicle_status2_g == 29:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm1.digital_output_load1()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))

            mm.setVoltage(DTH.convertohex(target_volatge_from_car1), CanId.CAN_ID_1)

            RUNNING_CURRENT = int(target_current_from_car1 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm.setCurrent(CanId.CAN_ID_1)
            mm.startModule(CanId.CAN_ID_1)
            mm.readModule_Voltage(CanId.CAN_ID_1)
            mm.readModule_Current(CanId.CAN_ID_1)
            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_load1()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 37 and vehicle_status2_g == 0 or vehicle_status1 == 35 and vehicle_status2_g == 0 or vehicle_status1 == 35 and vehicle_status2_g == 6 or vehicle_status1 == 37 and vehicle_status2_g == 6:
            mm.stopcharging(CanId.CAN_ID_1)
            mm.stopModule(CanId.CAN_ID_1)
            mm.stopModule(CanId.CAN_ID_2)
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1
            mm.digital_output_open_stop(CanId.CAN_ID_1)
            time.sleep(5)
            mm1.digital_output_open_fan()
            PECC.STATUS1_GUN1_DATA[0] = 0
        if vehicle_status1 == 37 and vehicle_status2_g == 35 or vehicle_status1 == 35 and vehicle_status2_g == 37 or vehicle_status1 == 35 and vehicle_status2_g == 35 or vehicle_status1 == 37 and vehicle_status2_g == 35:
            mm.stopcharging(CanId.CAN_ID_1)
            mm.stopModule(CanId.CAN_ID_1)
            mm.stopModule(CanId.CAN_ID_2)
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1
            mm.digital_output_open_stop(CanId.CAN_ID_1)
            time.sleep(5)
            mm1.digital_output_open_fan()
            PECC.STATUS1_GUN1_DATA[0] = 0

        if vehicle_status1 == 37 and vehicle_status2_g == 2 or vehicle_status1 == 37 and vehicle_status2_g == 13 or vehicle_status1 == 37 and vehicle_status2_g == 21 or vehicle_status1 == 37 and vehicle_status2_g == 29:
            mm.stopcharging(CanId.CAN_ID_1)
            mm.stopModule(CanId.CAN_ID_1)
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1
            mm1.digital_output_open_load1()
            PECC.STATUS1_GUN1_DATA[0] = 0

        if vehicle_status1 == 35 and vehicle_status2_g == 2 or vehicle_status1 == 35 and vehicle_status2_g == 13 or vehicle_status1 == 35 and vehicle_status2_g == 21 or vehicle_status1 == 35 and vehicle_status2_g == 29:
            mm.stopcharging(CanId.CAN_ID_1)
            mm.stopModule(CanId.CAN_ID_1)
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1
            PECC.STATUS1_GUN1_DATA()
            PECC.STATUS1_GUN1_DATA[0] = 0
