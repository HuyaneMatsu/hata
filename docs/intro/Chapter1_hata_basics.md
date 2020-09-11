# Hata basics

Similarly to other wrappers, Hata uses asynchronous environment.

Lets continue with a simple example and then explain what happens.

###### Basic client example

```py
from hata import Client, start_clients

TOKEN = ''
NekoBot = Client(TOKEN)


@NekoBot.events
async def ready(client):
    print(f'{client.full_name} ({client.id}) logged in')


@NekoBot.events
async def message_create(client, message):
    """Simple reply functionality based on message content."""
    if message.author.is_bot:
        return  # We will ignore messages from bot accounts

    lowercase_content = message.content.lower()

    if lowercase_content in ('owo', 'uwu', '0w0'):
        await client.message_create(message.channel, lowercase_content)

    elif lowercase_content.startswith('ayy'):
        await client.message_create(message.channel, 'lmao')


start_clients()

```

1.: We import `Client` and `start_clients` from the library. If you get
`ImportError` or `ModuleNotFoundError`, then the library is not correctly
installed. I personally prefer importing the used.

> The examples will follow the `import ... from ...` pattern, when importing
> from the library, but `import ...` works totally fine as well.

2.:  We import the `re` module and we define some regex, what we will use
later. Knowing regex is really usefull, when working with strings, so if you
do not already know it, you should check 
[it](https://docs.python.org/3/library/re.html) out.

3.: We create our `Client` instance. When creating it, we need to define at
least it's token, got from
[Discord's application page](https://discordapp.com/developers/applications).
It accepts other optional attributes too, like `intents`, `shard_count` or
a whole set of them, what you might need later.

4.: We use `client.events` as a decorator, what allows you to put different
handlers under different discord events. There are multiple ways of adding
them, some is [mentioned](#Adding-event-examples) later. These handlers are
ensured, when the respective event is received from Discord.

5.: The `ready` event is ensured after the client finished logged in. When it
happens, at the example we print out the client's full name and it's id. The
wrapper's required python version is 3.6, what means format string are a thing,
so the wrapper actively [supports](#Formatting-objects) it.

6.: The `message_create` is ensured every time when the client receives a
message. It is triggered after bot messages as well, so first of all we want
to filter them out. Then we check it, whether it's content contains any kind
of OwO. If it does, then we reply on it. if it does not, then we check whether
the content contains Ayy, if it does, we reply on it as well.

7.: At the end we run up our client(s) with calling the `start_clients`
function.

###### Adding event examples

Events can be added on multiple ways, here are some examples:

```py
@NekoBot.events
async def emoji_create(client, guild, emoji):
    pass
```

That's the same as doing:

```py
async def emoji_create(client, guild, emoji):
    pass

NekoBot.events(emoji_create)
```

Using a different name:

```py
async def random_name(client, guild, emoji):
    pass

NekoBot.events(random_name, name='emoji_create')
```


```py
@NekoBot.events(name='emoji_create')
async def random_name(client, guild, emoji):
    pass
```

There are other cases as well, but these should be enough for now.

When adding event handler, then type and arg-count is checked, so whenever you
would mess something up, it should raise an exception, like:

- `ValueError: Events must be coroutine functions!`
- `ValueError: Invalid argcount, expected 2, got 1.`
- `LookupError: Invalid Event name: 'owowhatsthis'.`

## Formatting objects

A lot of hata's types' instances, which represent a Discord object have
formatting support. Lets take a `User` object as example:

- no format code is the user's name itself.
- `f` format code means full name, so name with discriminator.
- `m` format code stands for mention.
- `c` format code stands for the date when the user was created.

These formattings are also available as attributes or properties too:

- `.name`
- `.full_name`
- `.mention`
- `.created_at`

The only difference is that `.created_at` returns `datetime` object, meanwhile
formatting with `'c'` returns `str`.

> `Client` instances, are valid users too and they support the same formatting
> codes as well.
