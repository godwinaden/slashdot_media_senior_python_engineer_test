import asyncio
import threading
from typing import Awaitable, TypeVar

T = TypeVar("T")


def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


_LOOP = asyncio.new_event_loop()
_LOOP_THREAD = threading.Thread(target=start_background_loop, args=(_LOOP,), daemon=True)
_LOOP_THREAD.start()


def asyncio_run(async_method: Awaitable[T], timeout=30):
    return asyncio.run_coroutine_threadsafe(async_method, _LOOP).result(timeout=timeout)


def asyncio_gather(*futures, return_exceptions=False):
    return asyncio.gather(*futures, loop=_LOOP, return_exceptions=return_exceptions)
