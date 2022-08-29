from collections import defaultdict
import aioserial
import asyncio
from binascii import unhexlify
from Crypto.Cipher import AES
from config import settings
import logging

from dsmr_parser.parsers import TelegramParser
from dsmr_parser.objects import Telegram
from dsmr_parser import telegram_specifications
from dsmr_parser.clients import settings as dsmr_settings
from .bytestream_buffer import BytestreamBuffer

logger = logging.getLogger(__name__)

TID_HOMIE_MAPPING = [
    {
        "tid": "ELECTRICITY_IMPORTED_TOTAL",
        "node": "energy",
        "attribute": "imported-total"
    }, {
        "tid": "ELECTRICITY_USED_TARIFF_1",
        "node": "energy",
        "attribute": "used-tariff-1"
    }, {
        "tid": "ELECTRICITY_USED_TARIFF_2",
        "node": "energy",
        "attribute": "used-tariff-2"
    }, {
        "tid": "ELECTRICITY_DELIVERED_TARIFF_1",
        "node": "energy",
        "attribute": "delivered-tariff-1"
    }, {
        "tid": "ELECTRICITY_DELIVERED_TARIFF_2",
        "node": "energy",
        "attribute": "delivered-tariff-2"
    }, {
        "tid": "CURRENT_ELECTRICITY_USAGE",
        "node": "power",
        "attribute": "current-usage"
    }, {
        "tid": "CURRENT_ELECTRICITY_DELIVERY",
        "node": "power",
        "attribute": "current-delivery"
    }
]


def _get_mapping(telegram_id: str) -> dict:
    for d in TID_HOMIE_MAPPING:
        if d['tid'] == telegram_id:
            return d

    raise ValueError(f"Telegram ID '{telegram_id}' not defined in mapping to data")


def decrypt_message(encrypted_telegram: bytearray, init_vector: bytearray) -> str:
    cipher = AES.new(unhexlify(settings.client.guek), AES.MODE_GCM, nonce=init_vector)
    telegram = cipher.decrypt(encrypted_telegram)
    return telegram


async def _get_message(aioserial_instance: aioserial.AioSerial, mb: BytestreamBuffer):
    """read from provided serial interface the data into a byte stream buffer

    Args:
        aioserial_instance (aioserial.AioSerial): configured serial interface
        mb (BytestreamBuffer): bytestream buffer which is used also as state machine
    """
    while True:
        data = await aioserial_instance.read_async(size=1)
        state = mb.push_byte(data)
        if (state == BytestreamBuffer.States.RESULT) or \
           (state == BytestreamBuffer.States.STATE_INVALID):
            return


async def read_client(queue: asyncio.Queue) -> None:
    serial_settings = getattr(dsmr_settings, settings.client.serial.settings)
    serial_settings["port"] = settings.client.serial.port
    aios = aioserial.AioSerial(**serial_settings)

    logger.debug("Starting client main loop for Sagemcom T210-D-r client")
    while True:
        # We always start with an empty buffer
        mb = BytestreamBuffer()
        await _get_message(aios, mb)
        data = defaultdict(dict)
        if mb.current_state == BytestreamBuffer.States.RESULT:
            tg = decrypt_message(
                mb.encrypted_telegram,
                mb.system_title + mb.binary_frame_counter
            )
            spec = getattr(telegram_specifications, settings.telegram_specification)
            parser = TelegramParser(spec)
            try:
                t = Telegram(tg.decode('ASCII'), parser, spec)
                for tid, value in t:
                    mapping = _get_mapping(tid)
                    # TODO: We do not use the unit information ...
                    data[mapping['node']][mapping['attribute']] = value
                await queue.put(data)
                logger.debug(f"{data}")
            # TODO: we catch here any exception
            except BaseException as e:
                print(e)
                print("")
