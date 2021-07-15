from hata import Client, Guild

TOKEN = ''

# The `slash` framework
#
# Your bot needs to have `applications.commands` scope in the guilds, or it's slash commands wont show up. Note, that
# if you have 50 or more bots in the guild, it still wont work.
Sakuya = Client(TOKEN,
    extensions = 'slash',
)

# Using `Guild.precreate(guild_id, ...)` is a great way to get a reference to a not yet loaded entity.
MY_GUILD = Guild.precreate(123456)

@Sakuya.events
async def ready(client):
    print(f'{client:f} is connected!')


# Slash commands can be registered with the `.interactions` decorator if the client has slash extension setuped.
#
# Passing `is_global=True` will make the command global. These commands are available in each guild and in dm as well.
# Global command updates are distributed after 1 hour.
@Sakuya.interactions(is_global=True)
async def ping():
    """A ping command"""
    return 'pong'


# `guild=...` parameter will make the command guild bound.
@Sakuya.interactions(guild=MY_GUILD)
async def ayaya():
    """Ayaya?"""
    return 'ayaya!'


# `client` and `event` parameters are passed to slash commands if required. They must be the first defined parameters.
@Sakuya.interactions(is_global=True)
async def message_me(client, event):
    channel = await client.channel_private_create(event.user)
    await client.message_create(channel, 'Hello!')
    
    return 'messaged'


# Extra parameters will be added to the application commands. These can be annotated with a tuple of their type and
# description.
@Sakuya.interactions(is_global=True)
async def id_(
        user: ('user', 'The user to lookup')
            ):
    """A ping command"""
    return user.id


# Use default values to mark a parameter as optional
@Sakuya.interactions(is_global=True)
async def id_(event,
        user: ('user', 'The user to lookup') = None,
            ):
    """Shows the user\'s id"""
    if user is None:
        user = event.user
    return user.id


# Choice parameters can be done by passing the choices as type.
WELCOME_MESSAGES = [
    ('meow', 'Welcome to us meow, we got free pats.'),
    ('horny', 'Welcome to our horny dungeon, hope you feeling great!'),
    ('game', 'I hope that you brought your danmaku skills.'),
]

@Sakuya.interactions(is_global=True)
async def welcome(event,
        user: ('user', 'The user to welcome'),
        message: (WELCOME_MESSAGES, 'The message to send'),
            ):
    return f'{event.user:m} welcomes {user:m} to the guild.\n{message}'


Sakuya.start()
