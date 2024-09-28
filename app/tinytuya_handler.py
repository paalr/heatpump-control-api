import tinytuya

class TinyTuyaHandler:
    def __init__(self, device_id, ip_address, local_key, version):
        self.device = tinytuya.Device(
            dev_id=device_id,
            address=ip_address,
            local_key=local_key,
            version=version
        )

    def get_status(self):
        return self.device.status()

    def turn_on(self):
        return self.device.set_value('1', True)

    def turn_off(self):
        return self.device.set_value('1', False)

    def get_temperature(self):
        # Retrieves inlet and water tank temperatures
        status = self.device.status()
        dps = status.get('dps', {})
        return {
            'current_temperature': dps.get('16'),  # Inlet temperature
            'water_tank_temperature': dps.get('25')  # Water tank temperature
        }

    def set_water_temperature(self, temperature):
        # Set water temperature
        return self.device.set_value('101', temperature)

    def set_cold_temperature(self, temperature):
        # Set cold temperature
        return self.device.set_value('102', temperature)

    def set_heat_temperature(self, temperature):
        # Set heat temperature
        return self.device.set_value('103', temperature)

    def set_auto_temperature(self, temperature):
        # Set auto temperature
        return self.device.set_value('104', temperature)

    def get_mode(self):
        # Get the current mode of the device
        status = self.device.status()
        return status.get('dps', {}).get('2')

    def set_mode(self, mode):
        # Set the mode of the device (e.g., "heat", "cold", "auto")
        valid_modes = ["water", "cold", "heat", "auto", "wac", "wah", "waa"]
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode. Valid modes are: {valid_modes}")
        return self.device.set_value('2', mode)
    
    def get_error_code(self):
        # Retrieve the status and check for an error code
        status = self.device.status()
        dps = status.get('dps', {})
        return dps.get('121', '')  # Return the error code or empty string if no error