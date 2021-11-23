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

Hata is an *async* [Discord API](https://discord.com/developers/docs/intro) wrapper written in Python named after
[Hata no Kokoro](https://en.touhouwiki.net/wiki/Hata_no_Kokoro).

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


## [Documentation](https://github.com/HuyaneMatsu/hata/tree/master/docs)

The library reference is available [*here*](https://www.astil.dev/project/hata/docs/hata) & the tutorials are
available [*here*](https://github.com/HuyaneMatsu/hata/blob/master/docs/topics/README.md).

## Usage

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
<h1></h1>

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
<h1></h1>

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
    """ping-pong"""
    return 'pong'

Seija.start()

wait_for_interruption()
```

> Note: You need to restart your client, or the slash command wont show up. If there are more than 50 integrations
> (bots) in a guild, some of the (integrations) bots wont be able to use slash commands. This is currently a Discord
> limitation.

<h1></h1>

*Hata leaves the main thread free, `client.start()` blocks it only till the client logs in (or fails it), although you
can still use the `start_clients()` function, what as it says, starts up all the non-running clients parallelly.*

*Sometimes leaving the main thread might cause problems when trying to shut down the bot(s). At this case, you might
want to use `wait_for_interruption()`, which disconnects the clients gracefully and closes the event loop on keyboard
interrupt.*

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
- [`Proxisha`](https://github.com/Technisha) \[Feature requests & Bug hunting\]
- [`Hime Esuto`](https://github.com/HimeEsuto) \[Bug hunting\]
- [`BrainDead`](https://github.com/albertopoljak) \[Documentation improvements\]
- [`Zeref`](https://github.com/Zeref-Draganeel) \[Features & Typos & Bug hunting\]
- [`vinam`](https://github.com/v1nam) \[Bug hunting\[asyncio extension\]\]
