import time

from base_reader import BaseReader
from constants import PECC
from constants_manager import ConstantsManager
from message_helper import Module1Message as mm1, Module2Message as mm2
from utility import bytetobinary, binaryToDecimal, DTH


class Vehicle2StatusReader(BaseReader):
    arbitration_id = 1537

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantsManager()
        self._binary_data = bytetobinary(data)

    def read_input_data(self):
        vs2 = bytetobinary(self.data)
        self._global_data.set_data_status_vehicle2(binaryToDecimal(int(vs2[0])))
        vehicle_status2 = binaryToDecimal(int(vs2[0]))
        print('vhst2', vehicle_status2)
        vehicle_status1_g = self._global_data.get_data_status_vehicle1()
        print('vhst1', vehicle_status1_g)

        tag_vol2 = binaryToDecimal(int(vs2[2] + vs2[1]))
        target_volatge_from_car2 = int(tag_vol2 / 10)

        tag_curr2 = binaryToDecimal(int(vs2[4] + vs2[3]))
        tag_curr22 = int(tag_curr2 / 10)
        target_current_from_car2 = int(tag_curr22 / 2)

        if vehicle_status2 == 2 and vehicle_status1_g == 2:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0

        if vehicle_status2 == 13 and vehicle_status1_g == 0 or vehicle_status2 == 13 and vehicle_status1_g == 6:
            PECC.LIMITS1_DATA[4] = 120
            PECC.LIMITS1_DATA[5] = 5
            PECC.LIMITS2_DATA[2] = 44
            PECC.LIMITS2_DATA[3] = 1
            mm2.digital_output_close_Gun2()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            PECC.STATUS1_GUN2_DATA[0] = 1

            cable_check_voltage2 = binaryToDecimal(int(vs2[7] + vs2[6]))

            if cable_check_voltage2 <= 500:
                mm1.lowMode1()
                mm2.lowMode2()
            if cable_check_voltage2 > 500:
                mm1.highMode1()
                mm2.highMode2()

            mm1.setVoltage1(DTH.convertohex(cable_check_voltage2))
            mm2.setVoltage2(DTH.convertohex(cable_check_voltage2))
            mm1.startModule1()
            mm2.startModule2()
            mm2.readModule_Voltage_2()

            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm2.stopcharging2()
                mm1.stopModule1()
                mm2.stopModule2()
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_stop2()
                time.sleep(5)
                mm2.digital_output_open_fan()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm2.stopcharging2()
                mm1.stopModule1()
                mm2.stopModule2()
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 13 and vehicle_status1_g == 2 or vehicle_status2 == 13 and vehicle_status1_g == 35 or vehicle_status2 == 13 and vehicle_status1_g == 37:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm1.stopModule1()
            mm2.digital_output_Gun2_load1()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            PECC.STATUS1_GUN2_DATA[0] = 1

            cable_check_voltage2 = binaryToDecimal(int(vs2[7] + vs2[6]))

            if cable_check_voltage2 <= 500:
                mm2.lowMode2()
            if cable_check_voltage2 > 500:
                mm2.highMode2()

            mm2.setVoltage2(DTH.convertohex(cable_check_voltage2))
            mm2.startModule2()
            mm2.readModule_Voltage_2()

            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm2.stopcharging2()
                mm2.stopModule2()
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_load2()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm2.stopcharging2()
                mm2.stopModule2()
                mm1.stopModule1()
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 13 and vehicle_status1_g == 13 or vehicle_status2 == 13 and vehicle_status1_g == 21 or vehicle_status2 == 13 and vehicle_status1_g == 29:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm2.digital_output_load2()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            PECC.STATUS1_GUN2_DATA[0] = 1

            cable_check_voltage2 = binaryToDecimal(int(vs2[7] + vs2[6]))

            if cable_check_voltage2 <= 500:
                mm2.lowMode2()
            if cable_check_voltage2 > 500:
                mm2.highMode2()

            mm2.setVoltage2(DTH.convertohex(cable_check_voltage2))
            mm2.startModule2()
            mm2.readModule_Voltage_2()

            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm2.stopcharging2()
                mm2.stopModule2()
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_load2()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm2.stopcharging2()
                mm2.stopModule2()
                mm1.stopModule1()
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 21 and vehicle_status1_g == 0 or vehicle_status2 == 21 and vehicle_status1_g == 6:
            PECC.LIMITS1_DATA[4] = 120
            PECC.LIMITS1_DATA[5] = 5
            PECC.LIMITS2_DATA[2] = 44
            PECC.LIMITS2_DATA[3] = 1
            mm2.digital_output_close_Gun2()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            if target_volatge_from_car2 <= 500:
                mm1.lowMode1()
            if target_volatge_from_car2 > 500:
                mm1.highMode1()

            mm1.setVoltage1(DTH.convertohex(int(target_volatge_from_car2)))
            mm2.setVoltage2(DTH.convertohex(int(target_volatge_from_car2)))

            RUNNING_CURRENT = int(target_current_from_car2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm1.setCurrent1()
            mm2.setCurrent2()
            mm1.startModule1()
            mm2.startModule2()
            mm2.readModule_Voltage_2()
            mm1.readModule_Current_1()
            mm2.readModule_Current_2()
            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm2.stopcharging2()
                mm1.stopModule1()
                mm2.stopModule2()
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_stop2()
                time.sleep(5)
                mm2.digital_output_open_fan()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm2.stopcharging2()
                mm1.stopModule1()
                mm2.stopModule2()
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 21 and vehicle_status1_g == 2 or vehicle_status2 == 21 and vehicle_status1_g == 35 or vehicle_status2 == 21 and vehicle_status1_g == 37:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm1.stopModule1()
            mm2.digital_output_Gun2_load1()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))

            mm2.setVoltage2(DTH.convertohex(int(target_volatge_from_car2)))

            RUNNING_CURRENT = int(target_current_from_car2 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm2.setCurrent2()
            mm2.startModule2()
            mm2.readModule_Voltage_2()
            mm2.readModule_Current_2()
            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm2.stopcharging2()
                mm2.stopModule2()
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_load2()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm2.stopcharging2()
                mm2.stopModule2()
                mm1.stopModule1()
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 21 and vehicle_status1_g == 13 or vehicle_status2 == 21 and vehicle_status1_g == 21 or vehicle_status2 == 21 and vehicle_status1_g == 29:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm2.digital_output_load2()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            PECC.STATUS1_GUN2_DATA[0] = 1

            mm2.setVoltage2(DTH.convertohex(int(target_volatge_from_car2)))

            RUNNING_CURRENT = int(target_current_from_car2 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm2.setCurrent2()
            mm2.startModule2()
            mm2.readModule_Voltage_2()
            mm2.readModule_Current_2()
            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm2.stopcharging2()
                mm2.stopModule2()
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_load2()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm2.stopcharging2()
                mm2.stopModule2()
                mm1.stopModule1()
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 29 and vehicle_status1_g == 0 or vehicle_status2 == 29 and vehicle_status1_g == 6:
            PECC.LIMITS1_DATA[4] = 120
            PECC.LIMITS1_DATA[5] = 5
            PECC.LIMITS2_DATA[2] = 44
            PECC.LIMITS2_DATA[3] = 1
            mm2.digital_output_close_Gun2()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            if target_volatge_from_car2 <= 500:
                mm1.lowMode1()
            if target_volatge_from_car2 > 500:
                mm1.highMode1()
            mm1.setVoltage1(DTH.convertohex(int(target_volatge_from_car2)))
            mm2.setVoltage2(DTH.convertohex(int(target_volatge_from_car2)))

            RUNNING_CURRENT = int(target_current_from_car2)
            self._global_data.set_data_running_current(RUNNING_CURRENT)

            mm1.setCurrent1()
            mm2.setCurrent2()
            mm1.startModule1()
            mm2.startModule2()
            mm2.readModule_Voltage_2()
            mm1.readModule_Current_1()
            mm2.readModule_Current_2()
            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm2.stopcharging2()
                mm1.stopModule1()
                mm2.stopModule2()
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_stop2()
                time.sleep(5)
                mm2.digital_output_open_fan()
                PECC.STATUS1_GUN2_DATA[0] = 8
            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm2.stopcharging2()
                mm1.stopModule1()
                mm2.stopModule2()
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 29 and vehicle_status1_g == 2 or vehicle_status2 == 29 and vehicle_status1_g == 35 or vehicle_status2 == 29 and vehicle_status1_g == 37:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm1.stopModule1()
            mm2.digital_output_Gun2_load1()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))

            mm2.setVoltage2(DTH.convertohex(int(target_volatge_from_car2)))

            RUNNING_CURRENT = int(target_current_from_car2 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm2.setCurrent2()
            mm2.startModule2()
            mm2.readModule_Voltage_2()
            mm2.readModule_Current_2()
            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm2.stopcharging2()
                mm2.stopModule2()
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_load2()
            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm2.stopcharging2()
                mm2.stopModule2()
                mm1.stopModule1()
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 29 and vehicle_status1_g == 13 or vehicle_status2 == 29 and vehicle_status1_g == 21 or vehicle_status2 == 29 and vehicle_status1_g == 29:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm2.digital_output_load2()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))

            mm2.setVoltage2(DTH.convertohex(int(target_volatge_from_car2)))

            RUNNING_CURRENT = int(target_current_from_car2 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm2.setCurrent2()
            mm2.startModule2()
            mm2.readModule_Voltage_2()
            mm2.readModule_Current_2()
            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm2.stopcharging2()
                mm2.stopModule2()
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_load2()
            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm2.stopcharging2()
                mm1.stopModule1()
                mm2.stopModule2()
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 37 and vehicle_status1_g == 0 or vehicle_status2 == 35 and vehicle_status1_g == 0 or vehicle_status2 == 37 and vehicle_status1_g == 6 or vehicle_status2 == 35 and vehicle_status1_g == 6:
            mm2.stopcharging2()
            mm1.stopModule1()
            mm2.stopModule2()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            PECC.STATUS1_GUN2_DATA[0] = 1
            mm2.digital_output_open_stop2()
            time.sleep(5)
            mm2.digital_output_open_fan()
            PECC.STATUS1_GUN2_DATA[0] = 0

        if vehicle_status2 == 37 and vehicle_status1_g == 37 or vehicle_status2 == 35 and vehicle_status1_g == 35 or vehicle_status2 == 37 and vehicle_status1_g == 35 or vehicle_status2 == 35 and vehicle_status1_g == 37:
            mm2.stopcharging2()
            mm1.stopModule1()
            mm2.stopModule2()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            PECC.STATUS1_GUN2_DATA[0] = 1
            mm2.digital_output_open_stop2()
            time.sleep(5)
            mm2.digital_output_open_fan()
            PECC.STATUS1_GUN2_DATA[0] = 0

        if vehicle_status2 == 37 and vehicle_status1_g == 2 or vehicle_status2 == 37 and vehicle_status1_g == 13 or vehicle_status2 == 37 and vehicle_status1_g == 21 or vehicle_status2 == 37 and vehicle_status1_g == 29:
            mm2.stopcharging2()
            mm2.stopModule2()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            PECC.STATUS1_GUN2_DATA[0] = 1
            mm2.digital_output_open_load2()
            PECC.STATUS1_GUN2_DATA[0] = 0

        if vehicle_status2 == 35 and vehicle_status1_g == 2 or vehicle_status2 == 35 and vehicle_status1_g == 13 or vehicle_status2 == 35 and vehicle_status1_g == 21 or vehicle_status2 == 35 and vehicle_status1_g == 29:
            mm2.stopcharging2()
            mm2.stopModule2()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            PECC.STATUS1_GUN2_DATA[0] = 1
            mm2.digital_output_open_load2()
            PECC.STATUS1_GUN2_DATA[0] = 0
