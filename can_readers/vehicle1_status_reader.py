import time

from base_reader import BaseReader
from constants import PECC
from constants_manager import ConstantsManager
from message_helper import Module1Message as mm1, Module2Message as mm2
from utility import bytetobinary, binaryToDecimal, DTH


class Vehicle1StatusReader(BaseReader):
    arbitration_id = 769

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantsManager()
        self._binary_data = bytetobinary(data)

    def read_input_data(self):
        vs1 = bytetobinary()
        self._global_data.set_data_status_vehicle1(binaryToDecimal(int(vs1[0])))
        vehicle_status1 = binaryToDecimal(int(vs1[0]))
        print('vhst1', vehicle_status1)
        vehicle_status2_g = self._global_data.get_data_status_vehicle2()
        print('vhst2', vehicle_status2_g)
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
                mm1.lowMode1()
                mm2.lowMode2()
            if cable_check_voltage1 > 500:
                mm1.highMode1()
                mm2.highMode2()

            mm1.setVoltage1(DTH.convertohex(cable_check_voltage1))
            mm2.setVoltage2(DTH.convertohex(cable_check_voltage1))
            mm1.startModule1()
            mm2.startModule2()
            mm1.readModule_Voltage_1()

            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                mm2.stopModule2()
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_stop1()
                time.sleep(5)
                mm1.digital_output_open_fan()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                mm2.stopModule2()
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 13 and vehicle_status2_g == 2 or vehicle_status1 == 13 and vehicle_status2_g == 37 or vehicle_status1 == 13 and vehicle_status2_g == 35:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm2.stopModule2()
            mm1.digital_output_Gun1_load2()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1

            cable_check_voltage1 = binaryToDecimal(int(vs1[7] + vs1[6]))

            if cable_check_voltage1 <= 500:
                mm1.lowMode1()

            if cable_check_voltage1 > 500:
                mm1.highMode1()

            mm1.setVoltage1(DTH.convertohex(cable_check_voltage1))

            mm1.startModule1()

            mm1.readModule_Voltage_1()

            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()

                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_load1()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                mm2.stopModule2()
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
                mm1.lowMode1()

            if cable_check_voltage1 > 500:
                mm1.highMode1()

            mm1.setVoltage1(DTH.convertohex(cable_check_voltage1))

            mm1.startModule1()

            mm1.readModule_Voltage_1()

            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()

                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_load1()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                mm2.stopModule2()
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
                mm2.lowMode2()

            if target_volatge_from_car1 > 500:
                mm2.highMode2()

            mm1.setVoltage1(DTH.convertohex(int(target_volatge_from_car1)))
            mm2.setVoltage2(DTH.convertohex(int(target_volatge_from_car1)))

            RUNNING_CURRENT = int(target_current_from_car1)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm1.setCurrent1()
            mm2.setCurrent2()
            mm1.startModule1()
            mm2.startModule2()
            mm1.readModule_Voltage_1()
            mm1.readModule_Current_1()
            mm2.readModule_Current_2()
            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                mm2.stopModule2()
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_stop1()
                time.sleep(5)
                mm1.digital_output_open_fan()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                mm2.stopModule2()
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 21 and vehicle_status2_g == 2 or vehicle_status1 == 21 and vehicle_status2_g == 35 or vehicle_status1 == 21 and vehicle_status2_g == 37:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm2.stopModule2()
            mm2.digital_output_Gun1_load2()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1

            mm1.setVoltage1(DTH.convertohex(int(target_volatge_from_car1)))

            RUNNING_CURRENT = int(target_current_from_car1 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm1.setCurrent1()
            mm1.startModule1()
            mm1.readModule_Voltage_1()
            mm1.readModule_Current_1()
            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_load1()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                mm2.stopModule2()
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

            mm1.setVoltage1(DTH.convertohex(int(target_volatge_from_car1)))

            RUNNING_CURRENT = int(target_current_from_car1 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm1.setCurrent1()
            mm1.startModule1()
            mm1.readModule_Voltage_1()
            mm1.readModule_Current_1()
            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_load1()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                mm2.stopModule2()
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
                mm2.lowMode2()

            if target_volatge_from_car1 > 500:
                mm2.highMode2()

            mm1.setVoltage1(DTH.convertohex(int(target_volatge_from_car1)))
            mm2.setVoltage2(DTH.convertohex(int(target_volatge_from_car1)))

            RUNNING_CURRENT = int(target_current_from_car1)
            self._global_data.set_data_running_current(RUNNING_CURRENT)

            mm1.setCurrent1()
            mm2.setCurrent2()
            mm1.startModule1()
            mm2.startModule2()
            mm1.readModule_Voltage_1()
            mm1.readModule_Current_1()
            mm2.readModule_Current_2()
            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                mm2.stopModule2()
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_stop1()
                time.sleep(5)
                mm1.digital_output_open_fan()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                mm2.stopModule2()
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 29 and vehicle_status2_g == 2 or vehicle_status1 == 29 and vehicle_status2_g == 35 or vehicle_status1 == 29 and vehicle_status2_g == 37:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm1.digital_output_Gun1_load2()
            mm2.stopModule2()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))

            mm1.setVoltage1(DTH.convertohex(int(target_volatge_from_car1)))

            RUNNING_CURRENT = int(target_current_from_car1 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm1.setCurrent1()
            mm1.startModule1()
            mm1.readModule_Voltage_1()
            mm1.readModule_Current_1()
            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_load1()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                mm2.stopModule2()
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

            mm1.setVoltage1(DTH.convertohex(int(target_volatge_from_car1)))

            RUNNING_CURRENT = int(target_current_from_car1 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm1.setCurrent1()
            mm1.startModule1()
            mm1.readModule_Voltage_1()
            mm1.readModule_Current_1()
            digitl_input = self._global_data.get_data()
            if digitl_input[3] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                PECC.STATUS1_GUN1_DATA[0] = 9
                mm1.digital_output_open_load1()

            if digitl_input[3] == '0':
                PECC.STATUS1_GUN1_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm1.stopcharging1()
                mm1.stopModule1()
                mm1.stopModule2()
                PECC.STATUS1_GUN1_DATA[0] = 1

        if vehicle_status1 == 37 and vehicle_status2_g == 0 or vehicle_status1 == 35 and vehicle_status2_g == 0 or vehicle_status1 == 35 and vehicle_status2_g == 6 or vehicle_status1 == 37 and vehicle_status2_g == 6:
            mm1.stopcharging1()
            mm1.stopModule1()
            mm2.stopModule2()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1
            mm1.digital_output_open_stop1()
            time.sleep(5)
            mm1.digital_output_open_fan()
            PECC.STATUS1_GUN1_DATA[0] = 0
        if vehicle_status1 == 37 and vehicle_status2_g == 35 or vehicle_status1 == 35 and vehicle_status2_g == 37 or vehicle_status1 == 35 and vehicle_status2_g == 35 or vehicle_status1 == 37 and vehicle_status2_g == 35:
            mm1.stopcharging1()
            mm1.stopModule1()
            mm2.stopModule2()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1
            mm1.digital_output_open_stop1()
            time.sleep(5)
            mm1.digital_output_open_fan()
            PECC.STATUS1_GUN1_DATA[0] = 0

        if vehicle_status1 == 37 and vehicle_status2_g == 2 or vehicle_status1 == 37 and vehicle_status2_g == 13 or vehicle_status1 == 37 and vehicle_status2_g == 21 or vehicle_status1 == 37 and vehicle_status2_g == 29:
            mm1.stopcharging1()
            mm1.stopModule1()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1
            mm1.digital_output_open_load1()
            PECC.STATUS1_GUN1_DATA[0] = 0

        if vehicle_status1 == 35 and vehicle_status2_g == 2 or vehicle_status1 == 35 and vehicle_status2_g == 13 or vehicle_status1 == 35 and vehicle_status2_g == 21 or vehicle_status1 == 35 and vehicle_status2_g == 29:
            mm1.stopcharging1()
            mm1.stopModule1()
            PECC.STATUS1_GUN1_DATA[2] = binaryToDecimal(int(vs1[2]))
            PECC.STATUS1_GUN1_DATA[1] = binaryToDecimal(int(vs1[1]))
            PECC.STATUS1_GUN1_DATA[3] = binaryToDecimal(int(vs1[3]))
            PECC.STATUS1_GUN1_DATA[4] = binaryToDecimal(int(vs1[4]))
            PECC.STATUS1_GUN1_DATA[0] = 1
            PECC.STATUS1_GUN1_DATA()
            PECC.STATUS1_GUN1_DATA[0] = 0
