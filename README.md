<h1 align="center">
    <b><a href="https://github.com/HuyaneMatsu/hata">Hata</a></b>
</h1>

<h5 align="center">
    A blazing fast Discord API wrapper that you can't deny
</h5>

<p align="center">
    <a href="https://discord.gg/3cH2r5d">Support</a> |
    <a href="https://www.astil.dev/project/hata/docs/hata">Documentation</a> |
    <a href="https://github.com/HuyaneMatsu/hata">Source</a>
</p>

<h1></h1>

### About

Hata is an *async* [Discord API](https://discord.com/developers/docs/intro) wrapper written in Python named after [Hata no Kokoro](https://en.touhouwiki.net/wiki/Hata_no_Kokoro).

<h1></h1>

#### Why hata?

- Multiple simultaneous clients

    Hata can run multiple clients from the same instance without sacrificing performance, all while being easy to code.

- Performant
    
    Fast concurrent code based on async/await paradigm with cache control, PyPy support and much more!

- Newest API features
    
    Whatever Discord decides to release/update/break Hata will support it natively in no time!

- 100% Python

    Built in Python! Easy to code, easy to read, easy to maintain.


<h1></h1>

#### Why not hata?

- Small community

    Hata has a small but, slowly growing community. The chance of getting help outside of our
    [cosy discord server](https://discord.gg/3cH2r5d) equals to zero.


## [Documentation](https://www.astil.dev/project/hata/docs/hata)

The library reference is available [*here*](https://www.astil.dev/project/hata/docs/hata) & the tutorial is available [*here*](https://github.com/HuyaneMatsu/hata/blob/master/docs/topics/README.md)

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
<h1></h1>

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
<h1></h1>

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

<h1></h1>
If you are wondering, how to start more clients, just put the two code snippet into the same file.


*Hata leaves the main thread free, [`client.start()`](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client#start) blocks it only till the client logs in (or fails it), although you
can still use the [`start_clients`](https://github.com/HuyaneMatsu/hata/blob/master/docs/examples/e02_multiple_clients/main.py) function, what as it says, starts up all the non-running clients parallelly, so go
ahead and start python with `-i` option, then interact with the clients from your interactive console in runtime.*

## Installation

To install Hata simply do

```shell
# Linux/OS X
$ python3 -m pip install hata

# Windows
$ python -m pip install hata

# Voice Support
$ python -m pip install hata[voice]
```
And you are good to go! Hata has native pypy support as well if you need some more speed!
<h1></h1>

## Dependencies

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

## Acknowledgements

Shout-Out to our brave testers, who are helping the most to improve Hata!

- `Nekosia` \[Grammar\]
- [`Mina Ashido`](https://github.com/Technisha) \[Feature requests & Bug hunting\]
- [`Hime Esuto`](https://github.com/HimeEsuto) \[Bug hunting\]
- [`BrainDead`](https://github.com/albertopoljak) \[Documentation improvements\]
- [`Zeref Draganeel`](https://github.com/Killua-Zoldyck-007) \[Features & Typos & Bug hunting\]
- [`vinam`](https://github.com/saiTama-max) \[Bug hunting\[asyncio extension\]\]
