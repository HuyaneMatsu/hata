## Introduction

If you came here, and found this file, you probably know what a Discord API
wrapper is all about. If you are new hata or to creating a bot you came to the
right place.

If you are new to Python then making a Discord bot (in any Python wrappers) is
probably a bad idea. Creating a decent bot require intermediate Python
knowledge. So to prevent frustration when learning, reading
the documentation or understanding the offered help - it is a great idea
to have a solid Python knowledge.

Hata should cover the whole open Discord API (oauth2 too) and it is designed
to make bots fast and easy and it also contains commonly used features between
bots.

The goal of this document is to give enough knowledge to understand how Hata
works. This introduction will drive you through some common use cases, 
until you have enough knowledge of the wrapper to be able to make more advanced and complex features and automate
command creation.

If you want to check
[references](../ref), we got them too.

### About Hata

Similarly to other wrappers hata runs the clients in an asynchronous environment
too. But not like other wrappers it uses an event thread and not simple event
loops. It makes integrating sync code easier, and also does not blocks the
main thread either. This feature can be used on multiple things, like running an
interpreter on the main thread or starting a webserver.

This asynchronous system has some downside too - it is not compatible with other
asynchronous libraries, but there's nothing to fear because the wrapper includes
everything. And you can also run other async event loops on the main thread.

The clients are at the service of the wrapper. Each request is executed trough
the clients, so methods like `channel.send` are not implemented.
*Clients*, huh? Yes the wrapper can run more clients at the same
time and they can execute requests through each other as well too. They
share resource between each other and they meet when an event is dispatched.
