import asyncio
from config import settings
from .homie import devices

write_sink_dict = {
    "ElectricSmartMeter": devices.ElectricSmartMeter,
    "HeatSmartMeter": devices.HeatSmartMeter,
    "DummySmartMeter": devices.DummySmartMeter
}


async def write_sink(queue: asyncio.Queue) -> None:
    """Containing the main loop for the write to sink task. It gets the data to
    published from the provided queue

    Args:
        queue (asyncio.Queue): queue on which the data is put as dictionary

    Examples:
        Provided an example dictionary as expected on the queue:

            {'node_1': {'attr_1': 23.4, 'attr_2': 'IMP_STATE'}
    """
    homie_device = write_sink_dict.get(settings.sink.homie.device_type)()

    while True:
        data = await queue.get()
        print("RECEIVED DATA!")
        print(data)
        homie_device.publish_data(data)
