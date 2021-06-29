## Introduction

Welcome, if you are new to Hata or to creating bots you came to the right place.

The goal of these introduction docs is to give you enough knowledge to understand how Hata
works. This introduction will guide you through some common use cases until you have
enough knowledge of the wrapper to be able to make more advanced and complex features.

If you are new to Python then making a Discord bot (in any Python wrapper) is
probably a bad idea. Creating a decent bot require intermediate Python knowledge,
so to prevent frustration when learning, reading the documentation or understanding the 
offered help - it is a great idea to have solid Python knowledge.

Hata wrapper itself should cover the whole open Discord API (OAuth2 too) and 
it is designed to make bots fast and easy to create, it also comes with many
additional functionality to make end-user life easier.

### About Hata

Similarly to other wrappers Hata runs the clients in an asynchronous environment.
But unlike other wrappers it uses its own event thread.
This makes integrating sync code easier but has some downside too - it is not completely
compatible with other asynchronous libraries, but there's nothing to fear because Hata 
either includes its own code (like Hata backend http which is similar to aiohttp) or
has support to run it (most of the things from asyncio should work).

One of the unique features of the wrapper is that it can run multiple clients at 
the same time and all of them can execute requests through each other as well.
The clients might be standalone but internally they all share the same resources.
