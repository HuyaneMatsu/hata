# Events (CommandProcesser)

At the previous chapter we did some basic event handling, but lets go deeper
now (uwu). The wrapper contains some nice predefined events which can be
easily integrated. This part of the introduction will walk you trough
the most useful one of them in detail.

```py
from hata import Client, start_clients, events

Neko = Client(TOKEN)

on_command = Neko.events(events.CommandProcesser('e!')).shortcut
        
@on_command
async def rate(client, message, content):
    # rigg it
    if message.author is client:
        rating = 10
    else:
        rating = message.author.id%11

    #if it is called from a guild, lets get the user's nick
    name_or_nick = message.author.name_at(message.guild)
    
    await client.message_create(message.channel, f'I rate {name_or_nick} {rating}/10.')

@on_command
async def default_event(client, message):
    if message.author.is_bot:
        return
    content = message.content
    if len(content)!=3: # filter out totally useless cases
        return
    
    content = content.lower()
    
    if content=='owo':
        result = 'OwO'
    elif content=='uwu':
        result = 'UwU'
    elif content=='0w0':
        result = '0w0'
    else:
        return
    
    await client.message_create(message.channel, result)

start_clients()
```

One of the most useful events is the `CommandProcesser`.
This event can be shortcutted (or joining with `with` works the same way).
These events can not be used with `@` because the `__call__` magic
method is already used when the object is called by a parser but their
shorcut is a wrapper for this.

> [CommandProcesser reference](https://github.com/HuyaneMatsu/hata/blob/master/docs/ref/CommandProcesser.md)
> contains more detailed information about itself

### Cases

This event implements 5 cases:
- [`waitfor`](#waitfor)
- [`commands`](#commands)
- [`invalid_command`](#invalid_command)
- [`command_error`](#command_error)
- [`mention_prefix`](#mention_prefix)
- [`default_event`](#default_event)

#### waitfor

We can wait for a `message_create` event at a `channel`. If we get a message
at the set channel then each of its waiters will be awaited.

Take care because nothing is filtered yet - filtering out bot message authors and
channels comes only after this.

#### commands

When you create an instance of the `CommandProcesser` you always need to
pass a `prefix`. It can be `str`, `list` or `tuple` of `str` or a `callable`
that will get called with the `message` and should return a `str` type prefix.

An additional argument at creation is `ignorecase` - by default it is `True`.
It makes the prefixes not case sensitive.

The commands names are not case sensitive.

At this step we try to parse the messages content to 3 parts:
- prefix
- command
- content

The content ends at the first linebreak or at its real end.

If the parsed `command` is a valid command then we will await it and pass 2
or 3 arguments to it depending how much arguments the command accepts. These
arguments are the following: the `client`, the `message` and the parsed
`content` (as optional).

If we did not find the prefix we move on the
[`mention_prefix`](#default_event), then on the
[`default_event`](#default_event) part.

If we found the prefix, but the command is invalid, we move on the
[`invalid_command`](#invalid_command) case.

#### invalid_command

If set, called when a user used our prefix but typed a not existing command.
It can be added as any other command. It's specific name is `invalid_command`.

```py
@on_command
async def invalid_command(client, message, command, content):
    pass
```

#### command_error

If set, it is called, when an exception occures at a command.

```py
@on_command
async def command_error(client, message, command, content, exception):
    pass
```

#### mention_prefix

By default at creating `CommandProcesser` the `mention_prefix` argument is
passed as `True`. It means that if our client is `@mentioned` at the start message
we will try to parse it to 3 parts:
- client's mention
- command
- content

If the parsing was successful we try to call the correct command but if we
can not find it we just move on.

#### default_event

Same as the normal `message_create`, but called only if nothing else picks up
the message.

### Usage

```py
# Single prefix case, with mentioning the optional arguments.
event = CommandProcesser(prefix='e!', ignorecase=True, mention_prefix=True)

# Add the event to the client
Neko.events(event)

# The event has `__event_name__` set to `'message_create'`. so it can pick
# it up at the right place.

# Now lets shortcut our event:
on_command = Neko.events.message_create.shortcut

# Or we can use `with` statement too, what does the same:
with Neko.events.message_create.shortcut as on_command:
    pass

# Add a normal command
@on_command
async def test(client, message, content): 
    await client.message_create(message.channel,'test')

# If you will not use the content option, you can just skip it
@on_command
async def test(client, message): 
    await client.message_create(message.channel,'test')

# Add a command with different name
@on_commad(case='print')
async def print_command(client, message, content):
    await client.message_create(message.channel, content)

# Define a command, then add it later
async def pat(client, message, content):
    await client.message_create(message.channel, f'{client:m} pats {message.author:f}')

on_command(pat)

# Add later with different name, both is valid
on_command(pat, 'patpat')
on_command(pat, case='patpatpat')
```

### Loading commands from other files

This is probably simpler as most of the people think, lets look into it!

#### cute_commands.py
```py
from hata import eventlist

cute_commands = eventlist()

@cute_commands
async def pat(client, message, content):
    await client.message_create(message.channel, f'{client:m} pats {message.author:f}')

@cute_commands(case='love')
async def send_love(client, message, content):
    channel = await client.channel_private_create(message.author)
    await client.message_create(channel, 'I love you :3')
```

### mainfile.py
```py
from hata import Client, start_clients, events
from cute_commands import cute_commands

Neko = Client(TOKEN)

on_command = Neko.events(events.CommandProcesser('e!')).shortcut
on_command.extend(cute_commands)

start_clients()
```
        
The type `eventlist` knows all the 3 main operation the same that our
`on_command` shortcut knows.
(`on_command` is just my preferable name so do not stick with it).
This 2 main operations are `__call__` and `.extend`.

Even if you add commands trough `eventlist` their argument count will still
be checked when the main event handler is extended with them.

Creating complex systems is easily solvable because we can add not only
functions as events and the client itself is always passed as the first
argument. If these options are not enough - you are smart enough to make
something awesome.
