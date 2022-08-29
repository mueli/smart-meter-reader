import asyncio
import logging
import serial
from collections import defaultdict

from config import settings
from .const import (
    DEFAULT_BAUDRATE,
    DEFAULT_TIMEOUT,
    DEFAULT_SCAN_INTERVAL,
    SENSORS
)
from .kamstrup import Kamstrup

logger = logging.getLogger(__name__)

CMD_HOMIE_MAPPING = [
    {
        "cmd": 60,
        "node": "energy",
        "attribute": "imported-total"
    }, {
        "cmd": 80,
        "node": "power",
        "attribute": "current-usage"
    }, {
        "cmd": 86,
        "node": "temperatures",
        "attribute": "temp1"
    }, {
        "cmd": 87,
        "node": "temperatures",
        "attribute": "temp2"
    }, {
        "cmd": 89,
        "node": "temperatures",
        "attribute": "temp-diff"
    }, {
        "cmd": 74,
        "node": "flow",
        "attribute": "flow"
    }, {
        "cmd": 68,
        "node": "flow",
        "attribute": "volume"
    }, {
        "cmd": 1004,
        "node": "ops",
        "attribute": "hour-counter"
    }
]


def _get_mapping(cmd: int) -> dict:
    for d in CMD_HOMIE_MAPPING:
        if d['cmd'] == cmd:
            return d

    raise ValueError(f"CMD {cmd} not defined in mapping to data")


async def read_client(queue: asyncio.Queue) -> None:
    serial_settings = {
        "port": settings.client.serial.port,
        "baudrate": DEFAULT_BAUDRATE,
        "timeout": DEFAULT_TIMEOUT
    }

    kamstrup = Kamstrup(**serial_settings)

    logger.debug("Starting client main loop for Kamstrup 403 client")
    while True:
        data = defaultdict(dict)
        for key, sensor in SENSORS.items():
            try:
                logger.debug("Reading sensor %s (%s)", sensor["name"], key)
                # TODO: Should we check if unit provided by kamstrup.py is matching the
                # unit we set in the DATA_DEFINITION?
                value, unit = kamstrup.readvar(sensor["command"])
                mapping = _get_mapping(sensor["command"])
                data[mapping['node']][mapping['attribute']] = value
            except (serial.SerialException) as exception:
                logger.error(
                    "Device disconnected or multiple access on port? \nException: %e",
                    exception,
                )
            except (Exception) as exception:  # pylint: disable=broad-except
                logger.error(
                    "Error reading %s \nException: %s", sensor["name"], exception
                )
        logger.debug(f"collected data dict: {data}")
        await queue.put(data)
        await asyncio.sleep(DEFAULT_SCAN_INTERVAL)
