# Original file from:
# https://github.com/golles/ha-kamstrup_403/blob/main/custom_components/kamstrup_403/const.py
# All credits belong to golles!

"""Constants for Kamstrup 403."""

# Base component constants
NAME = "Kamstrup 403"
DOMAIN = "kamstrup_403"
MODEL = "403"
MANUFACTURER = "Kamstrup"
ATTRIBUTION = "Data provided by Kamstrup 403 meter"

# Defaults
DEFAULT_BAUDRATE = 1200
DEFAULT_SCAN_INTERVAL = 60  # overwritten to short interval
DEFAULT_TIMEOUT = 2.0

# Sensors
SENSORS = {
    0x003C: {
        "name": "Heat Energy (E1)",
        "command": 60,
    },
    0x0050: {
        "name": "Power",
        "command": 80,
    },
    0x0056: {
        "name": "Temp1",
        "command": 86,
    },
    0x0057: {
        "name": "Temp2",
        "command": 87,
    },
    0x0059: {
        "name": "Tempdiff",
        "command": 89,
    },
    0x004A: {
        "name": "Flow",
        "command": 74,
    },
    0x0044: {
        "name": "Volume",
        "command": 68,
    },
    0x03EC: {
        "name": "HourCounter",
        "command": 1004,
    },
}
