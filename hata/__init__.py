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

The following example answers on `ping` message.

```py
from hata import Client, wait_for_interruption

Nue = Client('TOKEN')

@Nue.events
async def ready(client):
    print(f'{client:f} logged in.')

@Nue.events
async def message_create(client, message):
    if message.author.bot:
        return
    
    if message.content == 'ping':
        await client.message_create(message.channel, 'pong')

Nue.start()

wait_for_interruption()
```

An improved example using the `commands` extension to handle common use cases.

```py
from hata import Client, wait_for_interruption

Saki = Client('TOKEN', extensions = 'commands_v2', prefix = 's!')

@Saki.events
async def ready(client):
    print(f'{client:f} logged in.')

@Saki.commands
async def ping(client, message):
    return 'pong'

Saki.start()

wait_for_interruption()
```

Or use slash commands!

```py
from hata import Client, Guild, wait_for_interruption

GUILD = Guild.precreate(guild_id)

Seija = Client('TOKEN', extensions = 'slash')

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

> Note: You need to restart your client, or the slash command wont show up. If there are more than 50 integrations
> (bots) in a guild, some of the (integrations) bots wont be able to use slash commands. This is currently a Discord
> limitation.

Hata leaves the main thread free, `client.start()` blocks it only till the client logs in (or fails it), although you
can still use the `start_clients()` function, what as it says, starts up all the non-running clients parallelly.

Sometimes leaving the main thread might cause problems when trying to shut down the bot(s). At this case, you might
want to use `wait_for_interruption()`, which disconnects the clients gracefully and closes the event loop on keyboard
interrupt.

We got some `tutorials:https://www.astil.dev/project/hata/guides/` as well, please check them too!
"""
__version__ = '1.3.17'

from .discord import *
from .ext import *
from .utils import *

from .env import *


__all__ = (
    *discord.__all__,
    *ext.__all__,
    *utils.__all__,
    
    *env.__all__,
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
    from . import test_config
