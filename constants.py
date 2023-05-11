

class GunStatus:
    NO_CONNECTION = 0
    CABLE_CHECK = 13
    CONNECTION_ERR = 6
    PRE_CHARGE = 21
    CHARGING = 29
    STOP_CHARGE = [35, 37]
    CONNECTED = 2  #TODO: change the key to make it more appropriate for newly connected vehicle


class CanId:
    CAN_ID_1 = 0x02204000
    CAN_ID_2 = 0x02208000
    PECC_POWER_VOLTAGE_L2 = 0x604
    PECC_CURRENT_L2 = 0x605
    PECC_STATUS1_Gun2 = 0x602
    PECC_STATUS2_Gun2 = 0x603
    DIGITAL_OUT = 0x500
    STOP_GUN2 = 0x609
    PECC_POWER_VOLTAGE_L1 = 0x304
    PECC_CURRENT_L1 = 0x305
    PECC_STATUS1_GUN1 = 0x302
    PECC_STATUS2_GUN1 = 0x303
    STOP_GUN1 = 0x309


class PECC:
    STATUS1_GUN1_DATA = [0, 0, 0, 0, 0, 0, 0]
    STATUS2_GUN1_DATA = [0, 0, 0, 0, 0, 0, 0]
    LIMITS1_DATA = [220, 5, 16, 39, 120, 5, 0, 0]
    LIMITS2_DATA = [0, 0, 44, 1]
    STATUS1_GUN2_DATA = [0, 0, 0, 0, 0, 0, 0]
    STATUS2_GUN2_DATA = [0, 0, 0, 0, 0, 0, 0]
