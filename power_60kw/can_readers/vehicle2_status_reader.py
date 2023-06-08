import logging
import time

from base_reader import BaseReader
from constants import PECC, CanId
from power_60kw.constant_manager_60kw import ConstantManager60KW
from power_60kw.message_helper import Module2Message as mm2, ModuleMessage as mm
from utility import bytetobinary, binaryToDecimal, DTH

logger = logging.getLogger(__name__)


class Vehicle2StatusReader(BaseReader):
    arbitration_id = 1537

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager60KW()
        self._binary_data = bytetobinary(data)

    def read_input_data(self):
        logger.info('Read input for Vehicle-1 status')
        vs2 = self._binary_data
        self._global_data.set_data_status_vehicle2(binaryToDecimal(int(vs2[0])))
        vehicle_status2 = binaryToDecimal(int(vs2[0]))
        logger.info(f'Vehicle-2 status {vehicle_status2}')
        vehicle_status1_g = self._global_data.get_data_status_vehicle1()
        logger.info(f'Vehicle-1 status {vehicle_status1_g}')

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
                mm.lowMode(CanId.CAN_ID_1)
                mm.lowMode(CanId.CAN_ID_2)
            if cable_check_voltage2 > 500:
                mm.highMode(CanId.CAN_ID_1)
                mm.highMode(CanId.CAN_ID_2)

            mm.setVoltage(DTH.convertohex(cable_check_voltage2), CanId.CAN_ID_1)
            mm.setVoltage(DTH.convertohex(cable_check_voltage2), CanId.CAN_ID_2)
            mm.startModule(CanId.CAN_ID_1)
            mm.startModule(CanId.CAN_ID_2)
            mm.readModule_Voltage(CanId.CAN_ID_2)

            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm.digital_output_open_stop(CanId.CAN_ID_2)
                time.sleep(5)
                mm.digital_output_open_fan()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 13 and vehicle_status1_g == 2 or vehicle_status2 == 13 and vehicle_status1_g == 35 or vehicle_status2 == 13 and vehicle_status1_g == 37:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm.stopModule(CanId.CAN_ID_1)
            mm2.digital_output_Gun2_load1()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            PECC.STATUS1_GUN2_DATA[0] = 1

            cable_check_voltage2 = binaryToDecimal(int(vs2[7] + vs2[6]))

            if cable_check_voltage2 <= 500:
                mm.lowMode(CanId.CAN_ID_2)
            if cable_check_voltage2 > 500:
                mm.highMode(CanId.CAN_ID_2)

            mm.setVoltage(DTH.convertohex(cable_check_voltage2), CanId.CAN_ID_2)
            mm.startModule(CanId.CAN_ID_2)
            mm.readModule_Voltage(CanId.CAN_ID_2)

            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_load2()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_1)
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
                mm.lowMode(CanId.CAN_ID_2)
            if cable_check_voltage2 > 500:
                mm.highMode(CanId.CAN_ID_2)

            mm.setVoltage(DTH.convertohex(cable_check_voltage2), CanId.CAN_ID_2)
            mm.startModule(CanId.CAN_ID_2)
            mm.readModule_Voltage(CanId.CAN_ID_2)

            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_load2()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_1)
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
                mm.lowMode(CanId.CAN_ID_1)
            if target_volatge_from_car2 > 500:
                mm.highMode(CanId.CAN_ID_1)

            mm.setVoltage(DTH.convertohex(int(target_volatge_from_car2)), CanId.CAN_ID_1)
            mm.setVoltage(DTH.convertohex(int(target_volatge_from_car2)), CanId.CAN_ID_2)
            RUNNING_CURRENT = int(target_current_from_car2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm.setCurrent(CanId.CAN_ID_1)
            mm.setCurrent(CanId.CAN_ID_2)
            mm.startModule(CanId.CAN_ID_1)
            mm.startModule(CanId.CAN_ID_2)
            mm.readModule_Voltage(CanId.CAN_ID_2)
            mm.readModule_Current(CanId.CAN_ID_1)
            mm.readModule_Current(CanId.CAN_ID_2)
            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm.digital_output_open_stop(CanId.CAN_ID_2)
                time.sleep(5)
                mm.digital_output_open_fan()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 21 and vehicle_status1_g == 2 or vehicle_status2 == 21 and vehicle_status1_g == 35 or vehicle_status2 == 21 and vehicle_status1_g == 37:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm.stopModule(CanId.CAN_ID_1)
            mm2.digital_output_Gun2_load1()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))

            mm.setVoltage(DTH.convertohex(int(target_volatge_from_car2)), CanId.CAN_ID_2)

            RUNNING_CURRENT = int(target_current_from_car2 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm.setCurrent(CanId.CAN_ID_2)
            mm.startModule(CanId.CAN_ID_2)
            mm.readModule_Voltage(CanId.CAN_ID_2)
            mm.readModule_Current(CanId.CAN_ID_2)
            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_load2()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_1)
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

            mm.setVoltage(DTH.convertohex(int(target_volatge_from_car2)), CanId.CAN_ID_2)

            RUNNING_CURRENT = int(target_current_from_car2 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm.setCurrent(CanId.CAN_ID_2)
            mm.startModule(CanId.CAN_ID_2)
            mm.readModule_Voltage(CanId.CAN_ID_2)
            mm.readModule_Current(CanId.CAN_ID_2)
            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_load2()

            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_1)
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
                mm.lowMode(CanId.CAN_ID_1)
            if target_volatge_from_car2 > 500:
                mm.highMode(CanId.CAN_ID_1)
            mm.setVoltage(DTH.convertohex(int(target_volatge_from_car2)), CanId.CAN_ID_1)
            mm.setVoltage(DTH.convertohex(int(target_volatge_from_car2)), CanId.CAN_ID_2)

            RUNNING_CURRENT = int(target_current_from_car2)
            self._global_data.set_data_running_current(RUNNING_CURRENT)

            mm.setCurrent(CanId.CAN_ID_1)
            mm.setCurrent(CanId.CAN_ID_2)
            mm.startModule(CanId.CAN_ID_1)
            mm.startModule(CanId.CAN_ID_2)
            mm.readModule_Voltage(CanId.CAN_ID_2)
            mm.readModule_Current(CanId.CAN_ID_1)
            mm.readModule_Current(CanId.CAN_ID_2)
            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm.digital_output_open_stop(CanId.CAN_ID_2)
                time.sleep(5)
                mm.digital_output_open_fan()
                PECC.STATUS1_GUN2_DATA[0] = 8
            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 29 and vehicle_status1_g == 2 or vehicle_status2 == 29 and vehicle_status1_g == 35 or vehicle_status2 == 29 and vehicle_status1_g == 37:
            PECC.LIMITS1_DATA[4] = 188
            PECC.LIMITS1_DATA[5] = 2
            PECC.LIMITS2_DATA[2] = 150
            PECC.LIMITS2_DATA[3] = 0
            mm.stopModule(CanId.CAN_ID_1)
            mm2.digital_output_Gun2_load1()
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))

            mm.setVoltage(DTH.convertohex(int(target_volatge_from_car2)), CanId.CAN_ID_2)

            RUNNING_CURRENT = int(target_current_from_car2 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm.setCurrent(CanId.CAN_ID_2)
            mm.startModule(CanId.CAN_ID_2)
            mm.readModule_Voltage(CanId.CAN_ID_2)
            mm.readModule_Current(CanId.CAN_ID_2)
            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_load2()
            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_1)
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

            mm.setVoltage(DTH.convertohex(int(target_volatge_from_car2)), CanId.CAN_ID_2)

            RUNNING_CURRENT = int(target_current_from_car2 * 2)

            self._global_data.set_data_running_current(RUNNING_CURRENT)
            mm.setCurrent(CanId.CAN_ID_2)
            mm.startModule(CanId.CAN_ID_2)
            mm.readModule_Voltage(CanId.CAN_ID_2)
            mm.readModule_Current(CanId.CAN_ID_2)
            digitl_input = self._global_data.get_data()
            if digitl_input[5] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN2_DATA[0] = 9
                mm2.digital_output_open_load2()
            if digitl_input[5] == '0':
                PECC.STATUS1_GUN2_DATA[0] = 5

            if digitl_input[1] == '0' or digitl_input[2] == '1':
                mm.stopcharging(CanId.CAN_ID_2)
                mm.stopModule(CanId.CAN_ID_1)
                mm.stopModule(CanId.CAN_ID_2)
                PECC.STATUS1_GUN2_DATA[0] = 1

        if vehicle_status2 == 37 and vehicle_status1_g == 0 or vehicle_status2 == 35 and vehicle_status1_g == 0 or vehicle_status2 == 37 and vehicle_status1_g == 6 or vehicle_status2 == 35 and vehicle_status1_g == 6:
            mm.stopcharging(CanId.CAN_ID_2)
            mm.stopModule(CanId.CAN_ID_1)
            mm.stopModule(CanId.CAN_ID_2)
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            PECC.STATUS1_GUN2_DATA[0] = 1
            mm.digital_output_open_stop(CanId.CAN_ID_2)
            time.sleep(5)
            mm.digital_output_open_fan()
            PECC.STATUS1_GUN2_DATA[0] = 0

        if vehicle_status2 == 37 and vehicle_status1_g == 37 or vehicle_status2 == 35 and vehicle_status1_g == 35 or vehicle_status2 == 37 and vehicle_status1_g == 35 or vehicle_status2 == 35 and vehicle_status1_g == 37:
            mm.stopcharging(CanId.CAN_ID_2)
            mm.stopModule(CanId.CAN_ID_1)
            mm.stopModule(CanId.CAN_ID_2)
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            PECC.STATUS1_GUN2_DATA[0] = 1
            mm.digital_output_open_stop(CanId.CAN_ID_2)
            time.sleep(5)
            mm.digital_output_open_fan()
            PECC.STATUS1_GUN2_DATA[0] = 0

        if vehicle_status2 == 37 and vehicle_status1_g == 2 or vehicle_status2 == 37 and vehicle_status1_g == 13 or vehicle_status2 == 37 and vehicle_status1_g == 21 or vehicle_status2 == 37 and vehicle_status1_g == 29:
            mm.stopcharging(CanId.CAN_ID_2)
            mm.stopModule(CanId.CAN_ID_2)
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            PECC.STATUS1_GUN2_DATA[0] = 1
            mm2.digital_output_open_load2()
            PECC.STATUS1_GUN2_DATA[0] = 0

        if vehicle_status2 == 35 and vehicle_status1_g == 2 or vehicle_status2 == 35 and vehicle_status1_g == 13 or vehicle_status2 == 35 and vehicle_status1_g == 21 or vehicle_status2 == 35 and vehicle_status1_g == 29:
            mm.stopcharging(CanId.CAN_ID_2)
            mm.stopModule(CanId.CAN_ID_2)
            PECC.STATUS1_GUN2_DATA[2] = binaryToDecimal(int(vs2[2]))
            PECC.STATUS1_GUN2_DATA[1] = binaryToDecimal(int(vs2[1]))
            PECC.STATUS1_GUN2_DATA[3] = binaryToDecimal(int(vs2[3]))
            PECC.STATUS1_GUN2_DATA[4] = binaryToDecimal(int(vs2[4]))
            PECC.STATUS1_GUN2_DATA[0] = 1
            mm2.digital_output_open_load2()
            PECC.STATUS1_GUN2_DATA[0] = 0
