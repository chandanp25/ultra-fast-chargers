import logging

from base_reader import BaseReader
from constants import PECC
from power_240kw.constant_manager_240kw import ConstantManager240KW
from utility import bytetobinary, binaryToDecimal, DTH
from config_reader import ConfigManager

logger = logging.getLogger(__name__)

class PowerModuleReader(BaseReader):

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager240KW()
        self._diff_vol_current = None
        self._binary_data = bytetobinary(data)

    def read_input_data(self):
        self._diff_vol_current = binaryToDecimal(int(self._binary_data[1]))


class PMSetDataCurrentPeccStatus(PowerModuleReader):

    def __init__(self, data, pecc_status):
        super().__init__(data)
        self._pecc_status = pecc_status

    def read_input_data(self):
        super().read_input_data()
        bd = self._binary_data
        if self._diff_vol_current == 98:
            volatge_pe1 = binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7]))
            divide_vol = int(volatge_pe1) / 1000
            t1 = int(divide_vol) * 10
            vl = DTH.converttohexforpecc(hex(t1))
            self._pecc_status[1] = vl[0]
            self._pecc_status[0] = vl[1]


class PMSetDataCurrentPeccStatus1(PMSetDataCurrentPeccStatus):
    arbitration_id = int(ConfigManager().get_power_config('PS1_ID'))

    def __init__(self, data):
        pecc_status = PECC.STATUS2_GUN1_DATA
        super().__init__(data, pecc_status)

    def read_input_data(self):
        logger.info('Reading input for 240KW PECC-1 Status')
        bd = self._binary_data
        super().read_input_data()
        if self._diff_vol_current == 48:
            self._global_data.set_data_current_pe1(binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7])))


class PMSetDataCurrentPeccStatus2(PMSetDataCurrentPeccStatus):
    arbitration_id = int(ConfigManager().get_power_config('PS2_ID'))

    def __init__(self, data):
        pecc_status = PECC.STATUS2_GUN1_DATA
        super().__init__(data, pecc_status)

    def read_input_data(self):
        logger.info('Reading input for 240KW PECC-2 Status')
        bd = self._binary_data
        super().read_input_data()
        if self._diff_vol_current == 48:
            self._global_data.set_data_current_pe2(binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7])))


class PMSetDataCurrentPeccStatus3(PMSetDataCurrentPeccStatus):
    arbitration_id = int(ConfigManager().get_power_config('PS3_ID'))

    def __init__(self, data):
        pecc_status = PECC.STATUS2_GUN1_DATA
        super().__init__(data, pecc_status)

    def read_input_data(self):
        logger.info('Reading input for 240KW PECC-3 Status')
        bd = self._binary_data
        super().read_input_data()
        if self._diff_vol_current == 48:
            c_pe3 = binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7]))
            current_pe3 = int(int(c_pe3) / 1000)
            tc1 = int(self._global_data.get_data_current_pe1()) / 1000
            tc2 = int(self._global_data.get_data_current_pe2()) / 1000
            tot_current1 = int(current_pe3 + tc1 + tc2) * 10
            cu_vl_21 = DTH.converttohexforpecc(hex(tot_current1))
            self._pecc_status[3] = cu_vl_21[0]
            self._pecc_status[2] = cu_vl_21[1]


class PMSetDataCurrentPeccStatus4(PMSetDataCurrentPeccStatus):
    arbitration_id = int(ConfigManager().get_power_config('PS4_ID'))

    def __init__(self, data):
        pecc_status = PECC.STATUS2_GUN2_DATA
        super().__init__(data, pecc_status)

    def read_input_data(self):
        logger.info('Reading input for 240KW PECC-4 Status')
        bd = self._binary_data
        super().read_input_data()
        if self._diff_vol_current == 48:
            self._global_data.set_data_current_pe4(binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7])))


class PMSetDataCurrentPeccStatus5(PMSetDataCurrentPeccStatus):
    arbitration_id = int(ConfigManager().get_power_config('PS5_ID'))

    def __init__(self, data):
        pecc_status = PECC.STATUS2_GUN2_DATA
        super().__init__(data, pecc_status)

    def read_input_data(self):
        logger.info('Reading input for 240KW PECC-5 Status')
        bd = self._binary_data
        super().read_input_data()
        if self._diff_vol_current == 48:
            self._global_data.set_data_current_pe5(binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7])))


class PMSetDataCurrentPeccStatus6(PMSetDataCurrentPeccStatus):
    arbitration_id = int(ConfigManager().get_power_config('PS6_ID'))

    def __init__(self, data):
        pecc_status = PECC.STATUS2_GUN2_DATA
        super().__init__(data, pecc_status)

    def read_input_data(self):
        logger.info('Reading input for 240KW PECC-6 Status')
        bd = self._binary_data
        super().read_input_data()
        if self._diff_vol_current == 48:
            c_pe6 = binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7]))
            current_pe6 = int(int(c_pe6) / 1000)
            tc4 = int(self._global_data.get_data_current_pe4()) / 1000
            tc5 = int(self._global_data.get_data_current_pe5()) / 1000
            tot_current2 = int(current_pe6 + tc4 + tc5) * 10
            cu_vl_22 = DTH.converttohexforpecc(hex(tot_current2))
            self._pecc_status[3] = cu_vl_22[0]
            self._pecc_status[2] = cu_vl_22[1]
