from time import perf_counter

from hata import ClientWrapper


ALL = ClientWrapper()


@ALL.interactions(is_global = True, wait_for_acknowledgement = True)
async def ping():
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    delay = (perf_counter() - start) * 1000.0

    yield f'{delay:.0f} ms'
