
class ConstantsManager:
    __instance = None  # Private class variable to store the singleton instance

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, d='', pe1current=0, rc=0, vehiclestatus2=6, vehiclestatus1=6):
        self._digitalinput = d
        self._pe1_current = pe1current
        self._rc = rc
        self._vehicle_status2 = vehiclestatus2
        self._vehicle_status1 = vehiclestatus1
        
    def get_data(self):
        return self._digitalinput

    def set_data(self, x):
        self._digitalinput = x
    
    def get_data_current_pe1(self):
        return self._pe1_current

    def set_data_current_pe1(self, x):
        self._pe1_current = x

    def get_data_running_current(self):
        return self._rc

    def set_data_running_current(self, x):
        self._rc = x

    def get_data_status_vehicle2(self):
        return self._vehicle_status2

    def set_data_status_vehicle2(self,x):
        self._vehicle_status2 = x

    def get_data_status_vehicle1(self):
        return self._vehicle_status1

    def set_data_status_vehicle1(self,x):
        self._vehicle_status1 = x
