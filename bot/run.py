#!env/Scripts/python

import sys
import asyncio
import os
from concurrent.futures import ProcessPoolExecutor

from iiwb.bot import Bot

_reverse = Bot(description="If I Were a (discord) Bot", command_prefix=":", pm_help = False)

asyncio.run(_reverse.run(*sys.argv[1:]))