import asyncio
import math
import logging

logger = logging.getLogger(__name__)


async def read_client(queue: asyncio.Queue) -> None:
    percentage = 0
    logger.debug("Starting client main loop for Dummy client")
    while True:
        percentage += 1
        data = {"energy": {"imported-total": math.sin(2 * math.pi * percentage/100.0)}}
        await queue.put(data)
        await asyncio.sleep(2)
        if percentage == 100:
            percentage = 0
