"""
Hata is an async Discord API wrapper written in Python named after Hata no Kokoro.

Why hata
--------

- Multiple simultaneous clients

    Hata can run multiple clients from the same instance without sacrificing performance, all while being easy to code.

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
    if message.author.is_bot:
        return
    
    if message.content == 'ping':
        await client.message_create(message.channel, 'pong')

Nue.start()

wait_for_interruption()
```

An improved example using the `commands` extension to handle common use cases.

```py
from hata import Client, wait_for_interruption

Saki = Client('TOKEN', extensions='commands', prefix='s!')

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

Seija = Client('TOKEN', extensions='slash')

@Seija.events
async def ready(client):
    print(f'{client:f} logged in.')

@Seija.interactions(guild=GUILD)
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

We got some tutorials on `github:https://github.com/HuyaneMatsu/hata/tree/master/docs` as well, please check them too!
"""
__version__ = '1.1.122'

from .env import BACKEND_ONLY

from .backend import *

if BACKEND_ONLY:
    __all__ = backend.__all__

else:
    from .discord import *
    from .ext import *
    
    __all__ = (
        *backend.__all__,
        *discord.__all__,
        *ext.__all__,
    )

from .backend.export import check_satisfaction
check_satisfaction()
