# Introduction

If you are new to Python then making a Discord bot (in any Python wrapper) is probably a bad idea. Creating a decent
bot requires intermediate programming knowledge, so to prevent frustration when learning, reading the documentation or
understanding the offered help - it is a great idea to have solid knowledge.

## Hata

Hata is an asynchronous Discord API wrapper built on it's own asynchronous environment. It supports `asyncio` based
libraries thanks to it's `asyncio` extension. Integrating blocking code is made easy by built-in tools

Python versions from 3.6 till 3.10 are supported. It runs on both Cpython and PyPy interpreter as well.

Client instances provide top level methods for interacting with the Discord API. They both work with and without cache.
Gateway connection is not required.

Sharding is completely automatic and lightweight.

Cache is automatically updated as data is received. Updating entities is in focus allowing you to have object-life-long
up-to-date references.

The library runs best on Linux. Even tho it supports windows in general, many features are disabled, and
massively concurrent io is not recommended on it.

If you are keen, you might want to checkout the [example section](../examples).

#### Why hata?

- Multiple simultaneous clients

    Hata can run multiple clients from the same instance without sacrificing performance, all while being easy to code.

- Performant
    
    Fast concurrent code using async/await syntax, cache control, PyPy support and more!

- Newest API features
    
    Whatever Discord decides to release/update/break Hata will support it natively in no time!

- 100% Python

    Completely relies on Python! Easy to read, easy to understand, easy to code.

## Contributing

Issues and feature requests are always welcome. 

If you also want to contribute by pull requests, documentation improvements, bug fixes and other smaller changes
are welcome. For bigger changes please visit our Discord server and let's discuss it.

## Get in touch

If you have issues, suggestions, want to contribute, or just want to send cute neko pictures, join our discord server.

[![](https://discordapp.com/api/v9/guilds/388267636661682178/widget.png?style=banner1)](https://discord.gg/3cH2r5d)

## Dependencies

### Requirements

- Python >= 3.6
- [chardet](https://pypi.python.org/pypi/chardet) / [cchardet](https://pypi.org/project/cchardet/)

### Optional

- [dateutil](https://pypi.org/project/python-dateutil/)
- [PyNaCl](https://pypi.org/project/PyNaCl/) (for voice support)
- [brotli](https://pypi.org/project/Brotli/) / [brotlipy](https://pypi.org/project/brotlipy/)
