# Hata

Hata is an async Discord API wrapper written in Python named after Hata no Kokoro.

If naming a Discord API wrapper after a Touhou character is not enough to convince you to try it, it has got some
real stuff:

- Fast and simple asynchronous framework to write concurrent code using async/await syntax, but also great for
    embedding into a threaded system.
- Running more clients from the same instance.
- Shared entity cache between shards and clients.
- Feature rich API for common use cases.
- Fast rate limit handling.
- No member objects associated with guilds. Hata uses guild -> user -> guild relation enabling implementing
    cross-guild features more easily.
- Optimized dispatch event parsers depending on intents, client count and on handled events as well.
- Option to disable user presences or even user caching, although disabling user cache is not recommended.
- Command and extension loader extension.
- Audio sending and receiving.
- Can interacting with the Discord API without gateway connection.
- Switching between api version with environmental variable.

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

An improved example using the `commands` extension to handle common use cases.

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
    return 'pong'

Saki.start()
```

Or use slash commands!

```py
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

## Installing guide

To install the package use:

``` shell
# Linux/OS X
$ python3 -m pip install hata

# Windows
$ python -m pip install hata
```

Hata has native pypy support as well if you need some more speed!

#### Requirements

- Python >= 3.6
- [chardet](https://pypi.python.org/pypi/chardet) / [cchardet](https://pypi.org/project/cchardet/)

#### Optional requirements

- [dateutil](https://pypi.org/project/python-dateutil/)
- [PyNaCl](https://pypi.org/project/PyNaCl/) (for voice support)
- [brotli](https://pypi.org/project/Brotli/) / [brotlipy](https://pypi.org/project/brotlipy/)

## Join our server

If you have issues, suggestions, want to contribute, or just want to send cute neko pictures, join our discord server.

[![](https://discordapp.com/api/v8/guilds/388267636661682178/widget.png?style=banner1)](http://discord.gg/3cH2r5d)

## Acknowledgement

Shout-Outs for our brave testers, who are helping the most improving the library:

- `Nekosia#1359` \[Grammar\]
- [`Elizabeth Afton#3506`](https://github.com/Technisha) \[Feature requests & Bug hunting\]
- [`๖ۣۜひめ・エスト✧ 「Hime・Esuto」#5167`](https://github.com/HimeEsuto) \[Bug hunting\]
- [`BrainDead#6105`](https://github.com/albertopoljak) \[Documentation improvements\]
- [`Zeref Draganeel#9897`](https://github.com/Killua-Zoldyck-007) \[Features & Typos & Bug hunting\]
- [`vinam#6057`](https://github.com/saiTama-max) \[Bug hunting\[asyncio extension\]\]
