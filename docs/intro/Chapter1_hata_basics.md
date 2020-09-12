# Hata basics

Similarly to other wrappers, Hata uses asynchronous environment.

Lets continue with a simple example and then explain what happens.

## Basic client example

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

1.: We import `Client` and `start_clients` from the library.
If you get `ImportError` or `ModuleNotFoundError` then the library is not correctly installed.

2.: We define our TOKEN, which is a string.
You can get one by registering your Bot with [Discord's application page](https://discordapp.com/developers/applications)

**Note:** When creating your Discord bot application in Discord application page you should check both `presence intent`
and `server member` intent in order for this example to work. If you did not do this or you want just some specific
intents you can additionally pas `intents` kwarg to Client with value of 0 (default is `-1` which means ALL intents).

So for example `NekoBot = Client(TOKEN, intents=0)` and above example will work if you did not check intents in application page.

You can read more about which values represent what [here](https://github.com/HuyaneMatsu/hata/blob/0695fd613d76390c8668851631accc473031cc5c/hata/discord/parsers.py#L204)

You can read more about Discord intents [here](https://support.discord.com/hc/en-us/articles/360040720412)


3.: We create our `Client` instance and name it `NekoBot`. 
When creating it we need to pass at least a token but it accepts [other, optional, attributes too.](https://github.com/HuyaneMatsu/hata/blob/0695fd613d76390c8668851631accc473031cc5c/hata/discord/client.py#L607)

4.: We can use decorators on our client and here we use `@NekoBot.events` because our client is  named `NekoBot`.
In this case our decorator will capture `ready` event and handle it in `async def ready(client):` function.

The `ready` event will be activated after the client finished logging in to Discord.
When it happens, in the example above, we print out the client's full name and it's ID.

Event function can take multiple arguments depending on the event, but all of them take `client` as the first one.
The example we used is the most straightforward way but there are multiple ways of adding event handlers and there
are multiple events that you can register. You can read about this [Event Examples](#Event-examples).

5.: The `message_create` is called every time the client receives a message.
It is triggered by bot messages as well, so first of all we want to filter them out.
Then we lowercase the message content (message.content is the text of the message) and check if it contains certain words.
Functionality is simple, if someone writes either `owo`, `uwu` or `0w0` the bot will reply with the same message.
And if someone writes message that starts with `ayy` the bot will reply with `lmao`.

6.: At the end we run up our client(s) with calling the `start_clients` function.
This line will block until the client(s) successfully login, then it will return either True or False depending on success.

## Event examples

There are multiple events you can register,
you can take a look [here](https://github.com/HuyaneMatsu/hata/blob/0695fd613d76390c8668851631accc473031cc5c/hata/discord/parsers.py#L6011) to see all events.

You can register a event,  if you wish, in multiple ways so here are some examples:

This should be the most straightforward way:
```py
@NekoBot.events
async def emoji_create(client, emoji):
    pass
```

Above is the same as doing:

```py
async def emoji_create(client, emoji):
    pass

NekoBot.events(emoji_create)
```

Using a different name:

```py
async def random_name(client, emoji):
    pass

NekoBot.events(random_name, name='emoji_create')
```


```py
@NekoBot.events(name='emoji_create')
async def random_name(client, emoji):
    pass
```

There are other cases as well, but these should be enough for now.

When you add event handler the type and arg-count will be checked, so whenever you
would mess something up it will raise an exception like:

- `ValueError: Events must be coroutine functions!`
- `ValueError: Invalid argcount, expected 2, got 1.`
- `LookupError: Invalid Event name: 'owowhatsthis'.`

Examples for the above errors:

- `ValueError: Events must be coroutine functions!`
   Our function is not a coroutine, it is missing 'async' keyword to it.
    ```py
    @NekoBot.events
    def emoji_create(client, emoji):
        pass
    ```

- `ValueError: Invalid argcount, expected 2, got 1.`
   Our function took to many/little arguments.
    ```py
    # emoji_create should take 2 arguments, client and emoji
    @NekoBot.events
    async def emoji_create(client):
        pass
    ```

- `LookupError: Invalid Event name: 'owowhatsthis'.`
   We're trying to register a event that does not exist.
    ```py
    @NekoBot.events
    async def owowhatsthis(client):
        pass
    ```

## Formatting objects

A lot of hata's built-in types have formatting support.
Lets take `User` object that has name=test and discriminator=0007 as an example.

We can format it, for example, with an f-string: `print(f'{user:f}')`
which would result in `test#0007`

You can use these format codes:
- `f` format code means full name, so name with discriminator.
- `m` format code stands for mention.
- `c` format code stands for the creation date when the user was created.
- no format code is only the user name.

> `Client` instances are valid users too and they support the same formatting codes as well.

Note that you can also use object attributes too, in the case of `User` you would be able to use

- `.name`
- `.full_name`
- `.mention`
- `.created_at`
- etc

You should look up attributes for the object you're using to know more about them.
For now you can look trough the code or, while in our support Discord server, use command:
`&docs WHAT_TO_SERACH_FOR` specific example would be `&docs User`