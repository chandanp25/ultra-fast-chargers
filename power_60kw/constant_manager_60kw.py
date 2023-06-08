from base_constant_manager import BaseConstantManager


class ConstantManager60KW(BaseConstantManager):
    def __init__(self, d='', pe1current=0, rc=0, vehiclestatus2=6, vehiclestatus1=6):
        super().__init__(d, pe1current, vehiclestatus2, vehiclestatus1)
        self._rc = rc

    def get_data_running_current(self):
        return self._rc

    def set_data_running_current(self, x):
        self._rc = x
