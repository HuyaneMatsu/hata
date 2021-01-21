# -*- coding: utf-8 -*-
"""
Hata is an async Discord API wrapper written in Python named after Hata no Kokoro.

If naming a Discord API wrapper after a Touhou character is not enough to convince you to try it, it has got some real
stuff:

- Fast and simple asynchronous framework to write concurrent code using async/await syntax, but also great for
    embedding into a threaded system.
- Usage of Privileged Intents
- Running more clients from the same instance.
- Shared entity cache between shards and clients.
- Feature rich API for common use cases.
- Fast rate limit handling.
- No more member objects associated with guilds, if there is a user in more guilds, then there is only ONE user.
- Optimized dispatch event parsers depending on intents, client count and on handled events as well.
- Option to disable user presences or even user caching, although disabling user cache is not recommended.
- Command and extension loader extension.
- Audio sending and receiving.
- Can interacting with the Discord API without gateway connection.

Usage
-----

The following example answers on `ping` message.

```
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

```
from hata import Client
from hata.ext.commands import setup_ext_commands

Saki = Client('TOKEN')
setup_ext_commands(Saki, 's!')

@Saki.events
async def ready(client):
    print(f'{client:f} logged in.')

@Saki.commands
async def ping(client, message):
    return 'pong'

Saki.start()
```

Or use slash commands!

```
from hata import Client, Guild
from hata.ext.slash import setup_ext_slash

GUILD = Guild.precreate(guild_id)

Seija = Client('TOKEN')
setup_ext_commands(Seija)

@Seija.events
async def ready(client):
    print(f'{client:f} logged in.')

@Seija.interactions(guild=GUILD)
async def ping(client, event):
    return 'pong'

Seija.start()
```

If you wonder, how to run up more clients, just put the two code snippet into the same file.

Hata leaves the main thread free, `client.start()` blocks it only till the client logs in (or fails it), although you
can still use the `start_clients` function, what as it says, starts up all the non-running clients parallelly, so go
ahead and start python with `-i` option, then interact with the clients from your interactive console in runtime.
"""
__version__ = '1.1.34'

from .env import BACKEND_ONLY

if BACKEND_ONLY:
    from .backend import *
    __all__ = backend.__all__

else:
    from .backend import *
    from .discord import *
    
    __all__ = (
        *backend.__all__,
        *discord.__all__,
            )

