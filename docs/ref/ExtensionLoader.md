# class `ExtensionLoader`

There are some cases, when you propably want to change some functional part of
your client in runtime. Load, unload or reload code. Hata provides an easy to
use solution to solve this issue, it is called `ExtensionLoader`.

- Source : [extension_loader.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/extension_loader.py)

`ExtensionLoader` is an optional import, it will not be imported with the
library by default.

`ExtensionLoader` is a seperated extension from `events`, but it does
not means they dont go well together. But whats more, `ExtensionLoader` was
made to complement it.

## Usage

### Creating ExtensionLoader

An `ExtensionLoader` can be created, with passing just a client to it:

```py
extension_loader = ExtensionLoader(client)
```

### Adding extensions

After the client is passed, the extensions can be added:

```py
extension_loader.add('cute_commands')
```

Or more extensions can be added at the same time as well:

```py
extension_loader.add(['cute_commands', 'nice_commands'])
```

If an extension's file is not found, then `.add` will raise 
`ModuleNotFoundError`.

If the passed argument is not `str` instance or `iterable of str`, `TypeError`
is raised.

### Removing extensions

You can remove **not loaded** extensions from an extension loader.

```py
extension_loader.remove('cute_commands')
```

Removing more at the same time is supported as well:

```py
extension_loader.add(['cute_commands', 'nice_commands'])
```

If an extension's name is passed, what is not added, no errors will be raised.

If the passed argument is not `str` instance or `iterable of str`, `TypeError`
is raised.

### Entry and Exit points

When you add an extension, you should also pass an entry and an exit point
as well, or the loader will not call any specific function, when the loading
or  when the unloading finished.

`entry_point` is called, when the loading of an extension is done.
`exit_point` is called, when the extension is unloaded.

Theese points can be passed as `None` (default), `str` or a `callable`.
- If passed as `None`, no function will be called.
- If passed as `str`, the extension loader will try to get the function from
the extension with that name and call it with the `client`. If not found an
[`ExtensionError`](ExtensionError.md) will be raised. If found, but as `None`,
 it will be ignored.
- If passed as `callable`, then the extension loader will call it with the `client`
and with the extension (`module`).

> `entry_point` and `exit_point`-s always run on the client's thread and they
> can be coroutines as well.


##### String entry and exit point example

At cases, when a file needs a specific entry and exit point, like, when it adds
not only commands, but events as well, it can be usefull, to pass the entry
and the exit points as `str`, because you might want to change those runtime.

###### shiro.py

```py
from hata import Client, start_clients
from hata.extension_loader import ExtensionLoader
from hata import events

Shiro = Client(TOKEN) # lets give a name to our client now

# lets add some event handlers
Shiro.events(events.ReactionAddWaitfor)
Shiro.events(events.ReactionDeleteWaitfor)
Shiro.events(events.CommandProcesser('s|'))

extension_loader = ExtensionLoader(Shiro)
extension_loader.add('greetings', entry_point='entry', exit_point='exit')
extension_loader.load_all()

start_clients()
```

###### greetings.py

```py
from hata import eventlist

# when a user joins a guild, this event will be ensured.
async def guild_user_add(client, guild, user):
    
    # we want to send the welcoem message at the guild's system channel
    channel = guild.system_channel
    if channel is None:
        return
    
    # can we send message there?
    if not channel.cached_permissions_for(client).can_send_messages:
        return
       
    await client.message_create(channel, f'Welcome to the server {user:m}!')


# add some commands now
greeting_commands = eventlist()

@greeting_commands
async def hello(client, message, content):
    await client.message_create(message.channel, 'Hello there!')

@greeting_commands
async def cheers(client, message, content):
    await client.message_create(message.channel, 'Hype!')

# define the entry and the exit points

def entry(client):
    client.events(guild_user_add)
    client.events.message_create.shortcut.extend(greeting_commands)

    
def exit(client):
    del client.events.guild_user_add
    client.events.message_create.shortcut.unextend(greeting_commands)

```

##### Callable entry and exit point example

If more file is standardized and they use the same attribute names, it can be
usefull, to add more extensions with an already defined entry and exit points.

###### kuro.py

```py
from hata import Client, start_clients
from hata.extension_loader import ExtensionLoader
from hata import events

Kuro = Client(TOKEN) # shiro's pair is kuro

# lets add some event handlers
Kuro.events(events.ReactionAddWaitfor)
Kuro.events(events.ReactionDeleteWaitfor)
Kuro.events(events.CommandProcesser('k|'))

extension_loader = ExtensionLoader(Kuro)

def extension_entry(client, lib):
    client.events.message_create.shortcut.extend(lib.commands)

def extension_exit(client, lib):
    client.events.message_create.shortcut.unextend(lib.commands)
    
extension_loader.add(['interactions', 'infos'], entry_point=extension_entry, exit_point=extension_exit)
extension_loader.load_all()

start_clients()
```

##### interactions.py

```py
from hata import eventlist
from hata.events import ContentParser

commands = eventlist()

@commands
@ContentParser('user, flags=mni, default="message.author"')
async def hug(client, message, user):
    await client.message_create(message.channel, f'{client:m} *hugs* {user:m}')

@commands
@ContentParser('user, flags=mni, default="message.author"')
async def pat(client, message, user):
    await client.message_create(message.channel, f'{client:m} *pats* {user:m}')
```

##### infos.py

```py
from hata import eventlist, Embed
from hata.events import ContentParser

commands = eventlist()

@commands
@ContentParser('user, flags=mna, default="message.author"')
async def avatar(client, message, user):
    color = user.avatar&0xffffff
    if color==0:
        color = user.default_avatar.color

    url=user.avatar_url_as(size=4096)
    embed=Embed(f'{user:f}\'s avatar', color=color, url=url)
    embed.add_image(url)
    
    await client.message_create(message.channel, embed=embed)
    
@commands(case='guild-icon')
async def guild_icon(client, message, content):
    guild = message.guild
    if guild is None:
        # not guild channel -> leave
        return 
    
    icon_url = guild.icon_url_as(size=4096)
    if icon_url is None:
        embed=Embed(f'{guild.name} has no icon')
    else:
        color=guild.icon&0xffffff
        embed=Embed(f'{guild.name}\'s icon', url=icon_url, color=color)
        embed.add_image(icon_url)
    
    await client.message_create(message.channel, embed=embed)
```

### Loading, unloading and reloading extenions

The above examples show, how to load all the extensions, but there is more
behind that. The `ExtensionLoader`'s methods' names are not black magic.
Methods to work with extensions by name :`.load`, `.unload` and `.reload`.
Methods to work with all of the extensions: `.load_all`, `.unload_all`,
`.realod_all`.

Whenever any of theese methods is called, a `Task` will be returned, what 
runs on the client's loop (also wakes it up, if called from eslewhere).
The extension loader uses executors, to avoid  blocking operations, like
module loading (/realoding) or exception rendering, but the entry and the
exit points always run on the client's loop, as said above as well.

Tasks can be waited from non `EventThread`-s as well, like:

```py
extension_loader.load_all().syncwrap().wait()
```

If you want to run parts of the modules threadsafe, with the client's
`EventThread`, you can use `loop.enter()`, what pauses the loop meanwhile.

```py
from hata import KOKORO # the heart of the clients, a.k.a. their loop

with KOKORO.enter()
    # code goes here

```

> If you load extensions from extensions, be sure to not create lock loops,
> which will block threads forever.

##### Loading, unloading and reloading example

Lets continue the [`kuro`](#kuropy) example, with adding some more feautres
to it.

###### kuro.py (extended)

```py
from hata import Client, start_clients, Embed
from hata.extension_loader import ExtensionLoader, ExtensionError
from hata import events
from hata.events import Pagination

Kuro = Client(TOKEN) # shiro's pair is kuro

# lets add some event handlers
Kuro.events(events.ReactionAddWaitfor)
Kuro.events(events.ReactionDeleteWaitfor)

kuro_commands = Kuro.events(events.CommandProcesser('k|')).shortcut

extension_loader = ExtensionLoader(Kuro)


# Define loader, unloader and reloader command

@kuro_commands
async def load_extension(client, message, content):
    if not client.is_owner(message.author):
        return # owner only

    if content:
        try:
            await extension_loader.load(content)
        except ExtensionError as err:
            results = err.messages
        else:
            results = ['Extension loaded successfully.']
    
    else:
        try:
            await extension_loader.load_all()
        except ExtensionError as err:
            results = err.messages
        else:
            results = ['All extension loaded successfully.']

    embeds = [Embed(description=result) for result in results]
    
    await Pagination(client, message.channel, embeds)

@kuro_commands
async def unload_extension(client, message, content):
    if not client.is_owner(message.author):
        return # owner only

    if content:
        try:
            await extension_loader.unload(content)
        except ExtensionError as err:
            results = err.messages
        else:
            results = ['Extension unloaded successfully.']
    
    else:
        try:
            await extension_loader.unload_all()
        except ExtensionError as err:
            results = err.messages
        else:
            results = ['All extension unloaded successfully.']

    embeds = [Embed(description=result) for result in results]
    
    await Pagination(client, message.channel, embeds)

@kuro_commands
async def reload_extension(client, message, content):
    if not client.is_owner(message.author):
        return # owner only

    if content:
        try:
            await extension_loader.reload(content)
        except ExtensionError as err:
            results = err.messages
        else:
            results = ['Extension reloaded successfully.']
    
    else:
        try:
            await extension_loader.reload_all()
        except ExtensionError as err:
            results = err.messages
        else:
            results = ['All extension reloaded successfully.']

    embeds = [Embed(description=result) for result in results]
    
    await Pagination(client, message.channel, embeds)


def extension_entry(client, lib):
    kuro_commands.extend(lib.commands)

def extension_exit(client, lib):
    kuro_commands.unextend(lib.commands)
    
extension_loader.add(['interactions', 'infos'], entry_point=extension_entry, exit_point=extension_exit)

# we `.wait()` it, so if exception shows up, the client wont be started.
extension_loader.load_all().syncwrap().wait()

start_clients()

```

### Accessing extension loader from outside

Somtimes you want to access extension loader from other files as well. For
that case, an extension loader sets itself as an instance attribute of the
client as `client.extension_loader`. Also creating a second `ExtensionLoader`
on the same client will yield the old one.

> Whenever you call an extension loader on a client, what has an extension 
> loader of a different class, `RuntimeError` is (/should be) raised.

## Instance attributes

### `client`

- type : `weakref`

A weakreference to the extension loader's owner client, to avoid reference
loops. The wrapper supports runtime client adding and removing with full
cleanup, so this class should not deny it either.

### `extensions`

- type : `dict`
- items : (`str`, `Extension`)

A dict of the added extensions to the extension loader, where the keys are the
extensions' name and the values are the extensions.

## Methods

### `add(self, name, entry_point=None, exit_point=None)`

- returns : `None`
- raises : `TypeError` / `ModuleNotFoundError`

The method to add extensions to the extension loader.

`name` should be `str`, or an `iterable` of `str`-s, which contains
extension (module) names. `entry_point` and `exit_point` can be `None`, 
`str`, or a `callable`.

> If any inappropriate type is passed, a `TypeError` will be raised.

> If the extension is not found, a `ModuleNotFoundError` will be raised.

### `remove(self, name)`

- returns : `None`
- raises : `TypeError` / `RuntimeError`

Removes one or more extensions from the extension loader. If any of the 
extensions is not found, no errors will be raised.

`name` should be `str`, or an `iterable` of `str`-s, which contains
extension (module) names.

> If any inappropriate type is passed, a `TypeError` will be raised.

> If a loaded extension is requested for remove, `RuntimeError` will
> be raised.

### `load(self, name)`

- returns : `Task` -> `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`

Loads an extension with the given name. If anything goes wrong, raises
[`ExtensionError`](ExtensionError.md), which contains the traceback of the
> exception(s).

> If the extension is not found, an [`ExtensionError`](ExtensionError.md) will
> be raised.

> If the client is already deleted, `RuntimeError` will be raised.

### `unload(self, name)`

- returns : `Task` -> `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`

Unloads an extension with the given name. If anything goes wrong, raises
[`ExtensionError`](ExtensionError.md), which contains the traceback of the
exception(s).

If the extension is not loaded yet, will do nothing.

> If the extension is not found, an [`ExtensionError`](ExtensionError.md) will
> be raised.

> If the client is already deleted, `RuntimeError` will be raised.

### `reload(self, name)`

- returns : `Task` -> `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`

Reloads an extension with the given name. If anything goes wrong, raises
[`ExtensionError`](ExtensionError.md), which contains the traceback of the
exception(s).

If the extension is not loaded yet, will load it. if the extension is loaded,
will unload it first, then load it.

> If the extension is not found, an [`ExtensionError`](ExtensionError.md) will
> be raised.

> If the client is already deleted, `RuntimeError` will be raised.

### `load_all(self)`

- returns : `Task` -> `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`

Loads all the extension of the extension loader. If anything goes wrong,
raises an [`ExtensionError`](ExtensionError.md) only at the end, with the
exception(s).

> If the client is already deleted, `RuntimeError` will be raised.

### `unload_all(self)`

- returns : `Task` -> `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`

Unloads all the extension of the extension loader. If anything goes wrong,
raises an [`ExtensionError`](ExtensionError.md) only at the end, with the
exception(s).

> If the client is already deleted, `RuntimeError` will be raised.

### `reload_all(self)`

- returns : `Task` -> `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`

Reloads all the extension of the extension loader. If anything goes wrong,
raises an [`ExtensionError`](ExtensionError.md) only at the end, with the
exception(s).

> If the client is already deleted, `RuntimeError` will be raised.

## Magic methods

### `__new__(cls, client)`

- returns : [`ExtensionLoader`](ExtensionLoader.md)
- raises : `RuntimeError`

Creates an `ExtensionLoader` instance on the [client](Client.md). If the 
client has an extension loader already, returns that.

> If the client has an extension loader already, but with a differnt class,
> raises `RuntimeError`.

### `__repr__(self)`

- returns : `str`

Returns the representation of the extension loader.

### `_load(self, name)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`
- `awaitable`

[Loads](#_load_extensionself-client-extension-method) the given extension.
If the loading raises, the exception will contain every time only one message.

> If the extension is not found, an [`ExtensionError`](ExtensionError.md) will
> be raised.

> If the client is already deleted, `RuntimeError` will be raised.

### `_unload(self, name)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`
- `awaitable`

[Unloads](#_unload_extensionself-client-extension-method) the given extension.
If the unloading raises, the exception will contain every time only one message.

> If the extension is not found, an [`ExtensionError`](ExtensionError.md) will
> be raised.

> If the client is already deleted, `RuntimeError` will be raised.

### `_reload(self, name)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`
- `awaitable`

Reloads the given extension. First
[unloads](#_unload_extensionself-client-extension-method),
then [loads](#_load_extensionself-client-extension-method) it.
If unloading raises, wont try to load. The raised exception will contain every
time only one message.

> If the extension is not found, an [`ExtensionError`](ExtensionError.md) will
> be raised.

> If the client is already deleted, `RuntimeError` will be raised.

### `_load_all˙(self)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`
- `awaitiable`

Loads all the extensions of the extension loader. Will not load already loaded
extension. Loads each extension one after other. If any of the extensions 
raises, will still try to load the leftover ones. The raised exceptions'
messages are collected into one exception, what will be raised at the end.

> If the client is already deleted, `RuntimeError` will be raised.

### `_unload_all(self)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`
- `awaitable`

Unloads all the extensions of the extension loader. Will not unload not loaded,
or unloaded extensions. Unloads each extension one after the other. The raised
exceptions' messages are collected into one exception, what will be raised at
the end.  If any of the extensions raises, will still try to unload the
leftover ones. The raised exceptions' messages are collected into one
exception, what will be raised at the end.

> If the client is already deleted, `RuntimeError` will be raised.

### `_reload_all(self)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md) / `RuntimeError`
- `awaitiable`

Reloads all the extensions of the extension loader. If an extension is not
loaded, will load it, if the extension is loaded, will unload, then load it,
or if the extension is unload, will load it. Reloads each extension one after
the other. The raised exceptions' messages are collected into one exception,
what will be raised at the end.  If any of the extensions raises, will still
try to unload the leftover ones. The raised exceptions' messages are collected
into one exception, what will be raised at the end.

> If the client is already deleted, `RuntimeError` will be raised.

### `_load_extension(self, client, extension)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md)
- `awaitable`

Loads an extension to the client. If the extension is already loaded, will do 
nothing. The loading can be separated into 3 parts:

1. Loading the module.
2. Finding the entry point (if needed).
3. Ensuring the entry point.

If any of theese fails, an [`ExtensionError`](ExtensionError.md) will be
raised. If step 1 or 3 raises, then a traceback will be included.

### `_unload_extension(self, client, extension)` (method)

- returns : `None`
- raises : [`ExtensionError`](ExtensionError.md)
- `awaitable`

Unloads an extension from the client. If the extension is not loaded, will do
nothing. The unloading can be separated into 2 parts:

2. Finding the exit point (if needed).
3. Ensuring the exit point.

If any of theese fails, an [`ExtensionError`](ExtensionError.md) will be
raised. If step 2 raises, then a traceback will be included.

### `_render_exc(exception, header)` (staticmethod)

- returns : `str`

A function used to render exceptions' tracebacks. This function runs
in executor.
