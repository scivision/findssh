import os
import asyncio

from .coro import get_hosts
from .base import netfromaddress, getLANip

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
