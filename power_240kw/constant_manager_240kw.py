from base_constant_manager import BaseConstantManager


class ConstantManager240KW(BaseConstantManager):

    def __init__(self, d='', pe1current=0, pe2current=0, pe4current=0, pe5current=0, rc1=0, rc2=0, vehiclestatus2=6, vehiclestatus1=6 ):
        super().__init__(d, pe1current, vehiclestatus2, vehiclestatus1)
        self._pe2_current = pe2current
        self._pe4_current = pe4current
        self._pe5_current = pe5current
        self._rc1 = rc1
        self._rc2 = rc2

    def get_data_current_pe2(self):  # 240kW code change
        return self._pe2_current

    def set_data_current_pe2(self, x):
        self._pe2_current = x

    def get_data_current_pe4(self):  # 240kW code change
        return self._pe4_current

    def set_data_current_pe4(self, x):
        self._pe4_current = x

    def get_data_current_pe5(self):  # 240kW code change
        return self._pe5_current

    def set_data_current_pe5(self, x):
        self._pe5_current = x

    def get_data_running_current1(self): # 240kW code change
        return self._rc1

    def set_data_running_current1(self, x):
        self._rc1 = x

    def get_data_running_current2(self): # 240kW code change
        return self._rc2

    def set_data_running_current2(self, x):
        self._rc2 = x
