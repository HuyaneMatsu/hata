# Hata basics

Lets start instantly with a simple client example:

```py
from hata import Client,start_clients

client=Client(TOKEN)

@client.events
async def ready(client):
    print(f'{client:f} ({client.id}) logged in')

#we reply on uwu and on owo messages
@client.events
async def message_create(client,message):
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

Familiarly to other wrappers we use asynchronous environment and we can put
different functions under different discord events, which will be called
when the specific event occurs. There are 47 events defined right now.

Lets check some cases where we add events to a client:

```py
@client.events
async def event_name(client,*args):
    pass
```

That's the same as doing:
    
```py
async def event_name(client,*args):
    pass
client.events(event_name)
```

As expected we can use a custom name to:

```py
async def not_event_name(client,*args):
    pass
client.events(not_event_name,name='event_name')
```

An another case:

```py
@client.events.add(name='event_name')
async def not_event_name(client,*args):
    pass
```

There are other useful cases too, but lets not mention them right now.

Most of the classes have `__slots__` at the wrapper, so `client.event`'s
type has it too. That's an easy way to check each event's name. Also when
adding an event - type, arg-count and event name is checked so you should
get an exception which tells you what you messed up at adding a new event.

Some exception examples:

- `ValueError: Events must be coroutine functions!`
- `ValueError: Invalid argcount, expected 2, got 1 (args=False).`
- `LookupError: Invalid Event name: 'owowhatsthis'.`

## `ready` event

As you probably think - ready runs when the client logs in.
But actually ready is not a `ready-ready` event - it is called every time when
Discord sends a `READY` dispatch. It usually happens when Discord drops
the client, so it needs to reconnect. With some tricks you can check if the
client is `ready-ready` or just `ready`.

A useful API method to call when the client logs in is
`.update_application_info()` which allows you to access the `.owner`
property. Example:

```py
@client.events
async def ready(client):
    await client.update_application_info()
    print(f'My owner is : {client.owner:f}')
```

This method also loads every application info about the bot too. These
are stored at `.application` attribute.

An example where we call ready only once:

```py
@client.events
class ready:
    def __init__(self):
        self.called = False
        
    async def __call__(self,client):
        if self.called:
            return
        self.called = True
        
        await client.update_application_info()
        #do some stuffs
```

Events pick up on types or objects too and on their name. If it is a
type and it's initializer is async it will be stored as a type.
In every other case it initializes them and in this case the only condition 
is to have their `__call__` async.

## Comparing and formatting objects

A big speciality of the wrapper is that each Discord object
representation exists only once at the memory, so if you want to compare
two users like:

```py
if user1 == user2:
```

You should prefer using `is` over `==` :

```py
if user1 is user2:
```

The difference is that `==` compares their `id` but `is` compares their
address at the memory. The only case when you should use `==` instead of `is`
is when you want to compare webhook message authors because webhooks can
be sent using different avatars and names, so to check these
attributes each webhook's message's author might be a different object.

Also `>`, `>=`, `<=`, `<` works on Discord objects too - it compares
their `id` by default. But some types have `position` - like roles
or channels, so it will prefer comparing their position over the id.

An another speciality of the wrapper is that you can use special formatting
codes with f-strings. Lets take a `User` object as example:

- no format code is simply the user's name itself.
- `f` format code means full name, so name with discriminator.
- `m` format code stands for mention.
- `c` format code stands for the date when the user was created.

These formattings are also available as attributes or properties too:

- `.name`
- `.full_name`
- `.mention`
- `.created_at`

The only difference is `.created_at` returns `datetime` object instead of
`str`.
