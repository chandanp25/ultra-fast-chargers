import can

def settingCan():
	return can.interface.Bus(bustype='socketcan', channel='can1', bitrate=125000)

