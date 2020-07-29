# Hata

Hata is an async Discord API wrapper written in Python named after Hata no Kokoro.

If naming a Discord API wrapper after a Touhou character is not enough to convince you to try it, it got some
real stuff:

- Fast and simple asynchronous framework to write concurrent code using async/await syntax, but also great for
    embedding into a threaded system.
- Usage of [Privileged Intents](https://github.com/discordapp/discord-api-docs/issues/1363).
- Running more clients from the same instance.
- Shared entity cache between shards and clients.
- Feature rich API for common usacases.
- Fast ratelimit handling.
- No more member objects associated with guilds, if there is a user in more guilds, then there is only ONE user.
- Optimized dispatch event parsers depending on intents, client count and on handled events as well.
- Option to disable user presences or even user caching, although disabling user cache is not recommended.
- Command and extension loader extension.
- Audio sending and receiving.
- Can interacting with the Discord API without gateway connection.

## Usage

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

An improved example using the `commands` extension to handle common usecases.

```py

from hata import Client
from hata.ext.commands import setup_ext_commands

Saki = Client('TOKEN')
setup_ext_commands(Saki, 's!')

@Saki.events
async def ready(client):
    print(f'{client:f} logged in.')

@Saki.commands
async def ping(client, message):
    await client.message_create(message.channel, 'pong')

Saki.start()

```

If you wonder, how to run up more clients, just put the two code snippet into the same file.

Hata leaves the main thread free, `client.start()` blocks it only till the client logs in (or fails it), although you
can still use the `start_clients` function, what as it says, starts up all the non-running clients parallelly, so go
ahead and start python with `-i` option, then interact with the clients from your interactive console in runtime.

## Installing guide

To install the package use:

``` shell

# Linux/OS X
$ python3 -m pip install https://github.com/HuyaneMatsu/hata/archive/master.zip

# Windows
$ python -m pip install https://github.com/HuyaneMatsu/hata/archive/master.zip

```

#### Requirements

- Python >= 3.6
- [chardet](https://pypi.python.org/pypi/chardet) / [cchardet](https://pypi.org/project/cchardet/)

#### Optional requirements

- [dateutil](https://pypi.org/project/python-dateutil/)
- [PyNaCl](https://pypi.org/project/PyNaCl/) (for voice support)
- [brotli](https://pypi.org/project/Brotli/) / [brotlipy](https://pypi.org/project/brotlipy/)

## Join our server

If you have issues, suggestions, want to contribute, or just want to send cute neko pictures, join our discord server.

[![](https://discordapp.com/api/guilds/388267636661682178/embed.png?style=banner1)](http://discord.gg/3cH2r5d)

## Acknowledgement

The project is based on early versions of:
- [aiohttp](https://github.com/aio-libs/aiohttp)
- [asyncio](https://github.com/python/cpython/tree/master/Lib/asyncio)
- [discord.py](https://github.com/Rapptz/discord.py)
- [sqlalchemy_aoi](https://github.com/RazerM/sqlalchemy_aio)
- [trio](https://github.com/python-trio/trio)
- [websockets](https://github.com/aaugustin/websockets)
