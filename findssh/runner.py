import os
import sys
import asyncio


def runner(fun, *args):
    """
    Generic asyncio.run() equivalent for Python >= 3.5
    """
    if os.name == 'nt' and (3, 7) <= sys.version_info < (3, 8):
        asyncio.set_event_loop_policy(
            asyncio.WindowsProactorEventLoopPolicy()  # type: ignore
        )

    if sys.version_info >= (3, 7):
        result = asyncio.run(fun(*args))
    else:
        if os.name == 'nt':
            loop = asyncio.ProactorEventLoop()
        else:
            loop = asyncio.new_event_loop()
            asyncio.get_child_watcher().attach_loop(loop)
        result = loop.run_until_complete(fun(*args))
        loop.close()

    return result
