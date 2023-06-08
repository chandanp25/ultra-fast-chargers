from base_reader import BaseReader
from constants import PECC
from config_reader import ConfigManager
from power_60kw.constant_manager_60kw import ConstantManager60KW
from utility import bytetobinary, binaryToDecimal, DTH


class PowerModuleReader(BaseReader):

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager60KW()
        self._vehicle_status1_g = None
        self._vehicle_status2_g = None
        self._diff_vol_current = None
        self._binary_data = bytetobinary(data)

    def read_input_data(self):
        self._vehicle_status2_g = self._global_data.get_data_status_vehicle2()
        self._vehicle_status1_g = self._global_data.get_data_status_vehicle1()
        self._diff_vol_current = binaryToDecimal(int(self._binary_data[1]))


class PowerModule1Reader(PowerModuleReader):
    arbitration_id = ConfigManager().get_power_config('PS1_ID')

    def __init__(self, data):
        super().__init__(data)

    def read_input_data(self):
        super().read_input_data()
        if self._diff_vol_current == 98:
            bd = self._binary_data
            voltage_pe1 = binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7]))
            divide_vol = int(voltage_pe1) / 1000

            t1 = int(divide_vol) * 10
            print('voltage1=', t1)
            vl = DTH.converttohexforpecc(hex(t1))
            PECC.STATUS2_GUN1_DATA[1] = vl[0]
            PECC.STATUS2_GUN1_DATA[0] = vl[1]

        if self._diff_vol_current == 48:
            self._global_data.set_data_current_pe1(binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7])))
            if self._vehicle_status1_g == 21 and self._vehicle_status2_g != 0 and self._vehicle_status2_g != 6 or self._vehicle_status1_g == 29 and self._vehicle_status2_g != 0 and self._vehicle_status2_g != 6:
                pe1current = binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7]))
                c1 = int(int(pe1current) / 1000)
                current1 = int(c1) * 10
                cu_vl_1 = DTH.converttohexforpecc(hex(current1))
                PECC.STATUS2_GUN1_DATA[3] = cu_vl_1[0]
                PECC.STATUS2_GUN1_DATA[2] = cu_vl_1[1]


class PowerModule2Reader(PowerModuleReader):
    arbitration_id = ConfigManager().get_power_config('PS2_ID')

    def __init__(self, data):
        super().__init__(data)

    def read_input_data(self):
        super().read_input_data()
        if self._diff_vol_current == 98:
            bd = self._binary_data
            volatge_pe2 = binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7]))
            divide_vol2 = int(int(volatge_pe2) / 1000)
            t2 = int(divide_vol2) * 10
            print('voltage2=', t2)
            vl2 = DTH.converttohexforpecc(hex(t2))
            PECC.STATUS2_GUN2_DATA[1] = vl2[0]
            PECC.STATUS2_GUN2_DATA[0] = vl2[1]

        if self._diff_vol_current == 48:
            c_pe2 = binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7]))
            current_pe2 = int(int(c_pe2) / 1000)
            t = int(self._global_data.get_data_current_pe1()) / 1000
            if self._vehicle_status2_g == 0 or self._vehicle_status2_g == 6:
                tot_current1 = int(current_pe2 + t) * 10
                print('TOTAL CUERNET ===', tot_current1)
                cu_vl_21 = DTH.converttohexforpecc(hex(tot_current1))
                PECC.STATUS2_GUN1_DATA[3] = cu_vl_21[0]
                PECC.STATUS2_GUN1_DATA[2] = cu_vl_21[1]
            if self._vehicle_status1_g == 0 or self._vehicle_status1_g == 6:
                tot_current1 = int(current_pe2 + t) * 10
                print('TOTAL CUERNET ===', tot_current1)
                cu_vl_21 = DTH.converttohexforpecc(hex(tot_current1))
                PECC.STATUS2_GUN2_DATA[3] = cu_vl_21[0]
                PECC.STATUS2_GUN2_DATA[2] = cu_vl_21[1]
            if self._vehicle_status2_g == 21 and self._vehicle_status1_g != 0 and self._vehicle_status1_g != 6 or self._vehicle_status2_g == 29 and self._vehicle_status1_g != 0 and self._vehicle_status1_g != 6:
                tot_current2 = int(current_pe2) * 10
                cu_vl_22 = DTH.converttohexforpecc(hex(tot_current2))
                PECC.STATUS2_GUN2_DATA[3] = cu_vl_22[0]
                PECC.STATUS2_GUN2_DATA[2] = cu_vl_22[1]
