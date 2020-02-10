# class `CommandProcesser`

A predefined class to help out the bot devs with an already defined
`message_create` event.

- Source : [events.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/events.py)

Adding it to events is easy:
```py
client.events(CommandProcesser(PREFIX))
```

After adding it should be shortcutted with `with` statement or with
the [`.shortcut`](#shortcut) property.

```py
on_command=client.events.message_create.shortcut
```
or
```py
with client.events.message_create as on_command:
    #do stuffs
    pass
```

> If more handler is added `client.events.message_create`, then it will be
replaced with [`asynclist`](asynclist.md), but that datatype still supports
attribute lookup from it's element with overwriting `__getattr__`.

An important note might be, that [client.events](EventDescriptor.md) returns
the object after adding, so insta shortcut is the most elegant solution:

```py
on_command=client.events(CommandProcesser(PREFIX)).shortcut
```
Of cource `with` works as well.

## Creating the event

Because the class has an attribute, called `__event_name__` set to
`'message_create'` means, the [`EventDescriptor`](EventDescriptor.md) will
always pick it up at the correct place.

### `CommandProcesser(self,prefix,ignorecase=True,mention_prefix=True)`

- `prefix`

Prefix is the only required argument when creating this event. It can be `str`,
`list` or `tuple` of `str`, or a `callable`, what gets called with the
`message` and should return a prefix.

- `ignorecase = True`

If the event should not be case sensitive when checking the `prefix`.

- `mention_prefix = True`

By default when mentioning the client at the message's start will make the
event's parser to act, like the message's content was started with it's prefix.
But the main difference is that at this case if we fail to find the command, we
will not await the [`invalid_command`](#invalid_command) branch.

## Calling the event

### `client.events.message_create(client,message)`

We can separate the flow of the event's handling on 5 steps:
- [`waitfor`](#waitfor)
- [`commands`](#commands)
- [`invalid_command`](#invalid_command)
- [`command_error`](#command_error)
- [`mention_prefix`](#mention_prefix)
- [`default_event`](#default_event)

#### waitfor

We can wait for a `message_create` event at a
[`channel`](ChannelBase.md). If we get a [message](Message.md)
at the set channel, each of it's waiter will be awaited bound to it.

Take care, nothing is filtered yet, filtering out bot message authors and
channels, where we can not send messages comes only after this.

#### commands

At this step we try to parse the message's content to 3 parts:
- prefix
- command
- content

The commands' names are not case sensitive.

The content ends at the first linebreak, or at it's real end.

If the parsed `command` is a valid command, we will await it and pass 2
or 3 arguments to it, depends how much arguments the command accepts. These
arguments are the following: the `client`, the `message` and the parsed
`content` as optional too.

If we did not find the prefix we move on the
[`mention_prefix`](#default_event), then on the
[`default_event`](#default_event) part.

If we found the prefix, but the command is invalid, we move on the
[`invalid_command`](#invalid_command) case.

```py
@on_command #wrapping
async def owo(client, message, content):
    #do things
    pass

@on_command #content is optional
async def owo(client, message):
    #do things
    pass

on_command(owo) #simple adding

@on_command(case='uwu') #adding with differnt name
async def owo(client, message, content):
    #do things
    pass

on_command(owo,'uwu')       #adding with different name
on_command(owo,case='uwu')  #adding with different name


some_commads=eventlist() #creating just a simple container

@some_commads #all other adding option works
async def pat(client, message, content):
    # do things
    pass

@some_commands(case='hug') 
async def hug_command(client, message, content):
    # do things
    pass

on_command.extend(some_commads) #extending works too
```

If someone has no permissin to use a command (or such), then the command
should return a value what evaluates to `True`, because then the
[`CommandProcesser`](CommandProcesser.md) will act, like there is no command
with that name.

```py
from hata import Client
from hata.events import ContentParser

@on_command
@ContentParser('user, flags=mna, default="client"',)
async def update_application_info(client, message, user):
    if not client.is_owner(message.author):
        return True
    
    if type(user) is Client:
        await user.update_application_info()
        content = f'Application info of `{user:f}` is updated succesfully!'
    else:
         content = 'I can update application info only of a client.'
    
    await client.message_create(message.channel, content)
    
    return False
```

> Returning `False` is unnecesary, becuse `None` evaluates to `False` anyways,
> but it might look cleaner to return objects of just one datatype.

#### invalid_command

If set, called when a user used our prefix, but typed a not existing command.
It can be added as any other command. It's specific name is `invalid_command`.

```py
@on_command
async def invalid_command(client, message, command, content):
    #do things
    pass
```

#### command_error

Whenever an exception occures meanwhile awaiting a command,
[`client.events.error`](EventDescriptor.md#errorclienteventerr)
will be ensured, but an another handler can be added too to
[`CommandProcesser`](CommandProcesser.md).

```py
from io import StringIO

from hata import Embed
from hata.events import Pagination

@on_command
async def command_error(client, message, command, content, exception):
    with StringIO() as buffer:
        await client.loop.render_exc_async(exception, [
            client.full_name,
            ' ignores an occured exception at command ',
            repr(command),
            '\n\nMessage details:\nGuild: ',
            repr(message.guild),
            '\nChannel: ',
            repr(message.channel),
            '\nAuthor: ',
            message.author.full_name,
            ' (',
            repr(message.author.id),
            ')\nContent: ',
            repr(content),
            '\n```py\n'], '```', file=buffer)
        
        buffer.seek(0)
        lines = buffer.readlines()
    
    pages = []
    
    page_length = 0
    page_contents = []
    
    index = 0
    limit = len(lines)
    
    while True:
        if index == limit:
            embed = Embed(description=''.join(page_contents))
            pages.append(embed)
            page_contents = None
            break
        
        line = lines[index]
        index = index+1
        
        line_lenth = len(line)
        # long line check, should not happen
        if line_lenth > 500:
            line = line[:500]+'...\n'
            line_lenth = 504
        
        if page_length+line_lenth > 1997:
            if index == limit:
                # If we are at the last element, we dont need to shard up,
                # because the last element is always '```'
                page_contents.append(line)
                embed = Embed(description=''.join(page_contents))
                pages.append(embed)
                page_contents = None
                break
            
            page_contents.append('```')
            embed = Embed(description=''.join(page_contents))
            pages.append(embed)
            
            page_contents.clear()
            page_contents.append('```py\n')
            page_contents.append(line)
            
            page_length = 6+line_lenth
            continue
        
        page_contents.append(line)
        page_length += line_lenth
        continue
    
    limit = len(pages)
    index = 0
    while index<limit:
        embed = pages[index]
        index += 1
        embed.add_footer(f'page {index}/{limit}')
    
    await Pagination(client,message.channel,pages)
```

> Pagination uses different events too, so those should be added as well, to
> make this example work.

If exception occures at `command_error`, `client.events.error` will be ensured.
Same return applies to `command_error` as at [`commands`](#commands). If
`command_error` returns a value, what evaluates to `True`, then 
`client.events.error` will be called too, with the same exception. Can be
usefull for example if you want to show up exceptions only at a specific guild
or such.

#### mention_prefix

If our client is `@mentioned` at the start of the [message](Message.md),
we wil try to parse it to 3 parts:
- client's mention
- command
- content

If the parsing was successfull, we try to call the correct command, but if we
can not find it, we just move on.

#### default_event

Same as the normal `message_create` event. Awaited if non of the cases above
occurs.

```py
@on_command
async def default_event(client, message):
    #do things
    pass
```

## Adding events

The class the [`EventHandlerBase`](EventHandlerBase.md) class, what means
it can be `__enter__`-ed and `shortcut`-ted. When these happen, a bound
[`_EventCreationManager`](_EventCreationManager.md) is returned, what acts
like a wrapper for the [`__setevent__`](#__setevent__-__delevent__) method.

### `client.message_create.__setevent__(func,case)`

- raises : `TypeError` / `ValueError`

This method checks 3 cases:
- is `case` `'default_event'` and argcount is 2
- is `case` `'invalid_command'` and argcount is 4
- is `case` anything else and argcount is 2 or 3

If anything check fails, you might get some nice errors, like:
- `ValueError: 'default_event' expects 2 arguments (client, message).`
- `TypeError: Expected Coroutine function`
- `TypeError: Expected function, method, callable object`

## Removing events

Removing events is on the same way as adding.

### `client.message_create.__delevent__(func,case)`

- raises : `TypeError` / `ValueError`

First tries to find a command with the same name. If it found,
it will try to compare them.
if removing fails, raises `ValueError`

> Compares the two existing and the passed `func`, as it would be added as
> a command. If the passed `func` could not be even added as a command, will
> raise `TypeError`.

## Using waitfor

Waitfors are implemented with `WeakKeyDictionary`. Where The values are
`callables`, which should return an `awaitable` object. The keys are the
`wait where` objects, at this case [`channels`](ChannelBase.md).

### `client.events.message_create.append(wrapper, target)`

The `wrapper` is what will get called and the `target` is "where".
More `wrapper` can be added under the same `target` too. All of them will be
awaited in a reversed order, so if wrappers can safely remove themselves
meanwhile.

### `client.events.message_create.remove(wrapper, target)`

Same as adding but it removes the `wrapper`. Also raises no error, if the
`target` is "already" removed.

## Updating prefixes

If prefix is set with a callable, then it does not needs to be updated, except
if you want to update `ignorecase` at that case, If you passed before `str`,
`tuple` or `list` (yes, even at lists). 

Upadting `mention_prefix` is simpler, just modify the attribute.

### `client.events.message_create.update_prefix(prefix, ignorecase=None)`

Sets the event's prefix to the set value. If `ignorecase` is not passed as
`True` or `False`, it will use the previously set option.

### Superclasses

- [`EventHandlerBase`](EventHandlerBase.md)

## Instance attributes

| name              | description                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------|
| command_error     | The event, hat is called, when a command raised an exception.                                 |
| commands          | Dict of commands added to the event.                                                          |
| default_event     | The default event if prefix could not be parsed.                                              |
| ignorecase        | Is prefix not-case sensitive.                                                                 |
| invalid_command   | The event what called, when prefix found, but the corresponding command not.                  |
| mention_prefix    | Are we accepting mention too as prefix.                                                       |
| prefix            | The passed prefix at creation or at update.                                                   |
| prefixfilter      | The generated function to check the prefix at the start of the message and parse it's content.|
| waitfors          | A WeakKeyDictionary to store each waitfor, in (channel, callable) pair.                       |

## Properties

### `shortcut`

- returns : [`_EventCreationManager`](_EventCreationManager.md)

Normally the `CommandProcesser` cannot be used as a wrapper, because it's 
`__call__` is needed to handle the events.  This property returns a
[`_EventCreationManager`](_EventCreationManager.md) what acts
like a wrapper for the [`__setevent__`](#__setevent__-__delevent__) method.

## Methods

### `call_command(self,command_name,client,message,content='')`

- `awaitable`
- returns : `None`
- raises : `LookupError`

Looks up the command with the specific name. If the lookup fails, raises
`LookupError`.  If the command is found, will call it.

## Magic Methods

### `__enter__`, `__exit__`

Entering a `command_proceser` is same as [shortcutting](#shortcut) it.

### `__call__`

- `awaitable`
- returns : `None`

Handles the incoming event.

### `__setevent__`, `__delevent__`

The internal methods to set and del events from a
[`EventHandlerBase`](EventHandlerBase.md) "subclass".
