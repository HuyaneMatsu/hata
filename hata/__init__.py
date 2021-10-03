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


Why not hata
------------
- Small community
    
    Hata has a small and slowly increasing community. The chance of getting help outside of our
    `cosy discord server:https://discord.gg/3cH2r5d` equals to zero.

Usage
-----

The following example answers on `ping` message.

```py
from hata import Client

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
```

An improved example using the `commands` extension to handle common use cases.

```py
from hata import Client

Saki = Client('TOKEN', extensions='commands', prefix='s!')

@Saki.events
async def ready(client):
    print(f'{client:f} logged in.')

@Saki.commands
async def ping(client, message):
    return 'pong'

Saki.start()
```

Or use slash commands!

```py
from hata import Client, Guild

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
```

> Note: You need to restart your client, or the slash command wont show up. If there are more than 50 integrations
> (bots) in a guild, some of the (integrations) bots wont be able to use slash commands. This is currently a Discord
> limitation.

If you wonder, how to run up more clients, just put the two code snippet into the same file.

Hata leaves the main thread free, `client.start()` blocks it only till the client logs in (or fails it), although you
can still use the `start_clients` function, what as it says, starts up all the non-running clients parallelly, so go
ahead and start python with `-i` option, then interact with the clients from your interactive console in runtime.

We got some tutorials on `github:https://github.com/HuyaneMatsu/hata/tree/master/docs` as well, please check them too!
"""
__version__ = '1.1.108'

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
