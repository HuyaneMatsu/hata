"""
Hata is an asynchronous Discord API wrapper built on top of scarletio. It is designed to be easy to use, with also
providing rich API offering everything what an advanced developer might need.

Named after Hata no Kokoro from Touhou Project.

Why hata
--------

- Multiple simultaneous clients

    Hata can run multiple clients from the same instance without sacrificing performance.

- Performant
    
    Fast concurrent code using async/await syntax, cache control, PyPy support and more!

- Newest API features
    
    Whatever Discord decides to release/update/break Hata will support it natively in no time!

- 100% Python

    Completely relies on Python! Easy to read, easy to understand, easy to code.

Usage
-----

```py
from hata import Client, Guild, wait_for_interruption

GUILD = Guild.precreate(guild_id)

Seija = Client('TOKEN', extensions = ['slash'])

@Seija.events
async def ready(client):
    print(f'{client:f} logged in.')

@Seija.interactions(guild = GUILD)
async def ping():
    \"\"\"ping-pong\"\"\"
    return 'pong'

Seija.start()

wait_for_interruption()
```

Hata leaves the main thread free, `client.start()` blocks it only till the client logs in (or fails it), although you
can still use the `start_clients()` function, what as it says, starts up all the non-running clients parallelly.

Sometimes leaving the main thread might cause problems when trying to shut down the bot(s). At this case, you might
want to use `wait_for_interruption()`, which disconnects the clients gracefully and closes the event loop on keyboard
interrupt.

We got some `tutorials:https://www.astil.dev/project/hata/guides/` as well, please check them too!
"""
__version__ = '1.3.34'

# First import env, so if exception occurs we do not load the whole library.
from .env import *

from .discord import *
from .ext import *
from .utils import *


__all__ = (
    *discord.__all__,
    *env.__all__,
    *ext.__all__,
    *utils.__all__,
)

# Additional imports

import sys

from scarletio import check_satisfaction

from .utils.module_deprecation import get_deprecation_function

# Check whether every export is satisfied

check_satisfaction()

# Setup deprecations

__getattr__ = get_deprecation_function()

# Setup tests

if 'vampytest' in sys.modules:
    from . import vampytest_config
