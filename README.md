# Hata

Hata is an async Discord API wrapper written in Python named after Hata no Kokoro.

#### Why hata?

- Multiple simultaneous clients

    Hata can run multiple clients from the same instance without sacrificing performance, all while being easy to code.

- Performant
    
    Fast concurrent code using async/await syntax, cache control, PyPy support and more!

- Newest API features
    
    Whatever Discord decides to release/update/break Hata will support it natively in no time!

- 100% Python

    Completely relies on Python! Easy to read, easy to understand, easy to code.


#### Why not hata?

- Small community
    
    Hata has a small and slowly increasing community. The chance of getting help outside of our
    [cosy discord server](https://discord.gg/3cH2r5d) equals to zero.


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
    """ping-pong"""
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

## Installing guide

To install the package use:

```shell
# Linux/OS X
$ python3 -m pip install hata

# Windows
$ python -m pip install hata
```

Hata has native pypy support as well if you need some more speed!

### Dependencies

#### Requirements

- Python >= 3.6
- [chardet](https://pypi.python.org/pypi/chardet) / [cchardet](https://pypi.org/project/cchardet/)

#### Optional

- [dateutil](https://pypi.org/project/python-dateutil/)
- [PyNaCl](https://pypi.org/project/PyNaCl/) (for voice support)
- [brotli](https://pypi.org/project/Brotli/) / [brotlipy](https://pypi.org/project/brotlipy/)

## Get in touch

If you have issues, suggestions, want to contribute, or just want to send cute neko pictures, join our discord server.

[![](https://discordapp.com/api/v9/guilds/388267636661682178/widget.png?style=banner1)](https://discord.gg/3cH2r5d)

## Acknowledgement

Shout-Outs for our brave testers, who are helping the most improving the library:

- `Nekosia` \[Grammar\]
- [`Mina Ashido`](https://github.com/Technisha) \[Feature requests & Bug hunting\]
- [`Hime Esuto`](https://github.com/HimeEsuto) \[Bug hunting\]
- [`BrainDead`](https://github.com/albertopoljak) \[Documentation improvements\]
- [`Zeref Draganeel`](https://github.com/Killua-Zoldyck-007) \[Features & Typos & Bug hunting\]
- [`vinam`](https://github.com/saiTama-max) \[Bug hunting\[asyncio extension\]\]
