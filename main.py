from config_reader import ConfigManager


if __name__ == "__main__":
    config_mgr = ConfigManager()
    total_power = config_mgr.get_total_power()
    config_mgr.set_power(total_power)

    if int(total_power) == 60:
        from power_60kw.dynamicsharing import perform_action
    elif int(total_power) == 240:
        from power_240kw.dynamicsharing import perform_action
    perform_action()
