# Setup

Let's code our first hata bot!

If you haven't install hata yet, start a terminal and type:

```sh
python3 -m pip install hata
```

Or if using windows:

```sh
python -m pip install hata
```

# Writing your first bot

When creating your first bot make sure to enable all intents on the developer portal for the full experience.

Create a `main.py` file (any other name also works).

```py3
# Importing `Client` and `wait_for_interruption` from hata
from hata import Client, wait_for_interruption


# Creating your client (or bot)!
client = Client('super secret token comes here')


# When the bot finished logging in, its `ready` event handler is called.
# You can register event handlers, with the `@client.events` decorator.
@client.events
async def ready(client):
    print('Ready!')


# Connect (or login) to Discord!
client.start()


# Disconnect your bot gracefully when keyboard interrupt is received
wait_for_interruption()
```

Pretty simple! Now try running `python3 main.py` and you should see your bot online. Great success!

This is already pretty cool, but the bot does nothing yet. Let's make a simple ping-pong command.

```py3
# ... rest of the code

# Handle the message creation event
@client.events
async def message_create(client, message):
    # For now you will need just the text of the message. It can be accessed using `message.content`.
    # Lets compare that to '!ping' and reply on the with 'Ping!'
    
    if message.content == '!ping':
        await client.message_create(message, 'Pong!')


client.start()

wait_for_interruption()

```

Try running the bot and message it with `!ping`.

Got stuck? This is our resulting code:

```py3
from hata import Client, wait_for_interruption


client = Client('super secret token comes here')


@client.events
async def ready(client):
    print('Ready!')


@client.events
async def message_create(client, message):
    if message.content == '!ping':
        await client.message_create(message, 'Pong!')


client.start()

wait_for_interruption()
```

# Slash commands

This is a good start, but let's define some **real** commands using Discord's slash command feature.

For these commands you will need your bot to have `applications.commands` oauth2 scope in the guild.
If you invited your bot without it, no worries, go back to the [getting started](./getting_started.md) part and
look up there how to do it.

Hata has an already pre-made slash (and other interaction handling). It makes registering and
handling commands easy. To add the extension to your client use the `extensions` parameter like `extensions = 'slash'`.

```py3
from hata import Client, wait_for_interruption

# Add the `slash` extension to our client.
client = Client('super secret token comes here', extensions = 'slash')


@client.events
async def ready(client):
    print('Ready!')


# To register a slash command, use `@client.interactions` decorator.
#
# To register a command to your guild, use the `guild = guild_id` or `guild = guild` keyword parameter.
# To register a global command, use the `is_global = True` parameter. Note that global commands can take up to
# 1 hour to show up.
@client.interactions(guild = your_guilds_id)
async def ping():
    return 'Pong!'


client.start()

wait_for_interruption()
```

Great success! This not only looks cleaner, but there are many more options to customize your commands and their
parameters as well!

## What's next?

Considered creating slash commands? Check out our detailed [slash](slash.md) extension guide.

----

<p align="left">
    <a href="./introduction_to_python.md">Previously: Introduction to Python</a>
</p>
