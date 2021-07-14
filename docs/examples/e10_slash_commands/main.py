from hata import Client, Guild

TOKEN = ''

Sakuya = Client(TOKEN,
    extensions='slash',
)

MY_GUILD = Guild.precreate(123456)

@Sakuya.events
async def ready(client):
    print(f'{client:f} is connected!')


@Sakuya.interactions(is_global=True)
async def ping():
    """A ping command"""
    return 'pong'


@Sakuya.interactions(is_global=True)
async def id_(
        user : ('user', 'The user to lookup')
            ):
    """A ping command"""
    return user.id

@Sakuya.interactions(is_global=True)
async def id_(
        user : ('user', 'The user to lookup')
            ):
    """A ping command"""
    return user.id

WELCOME_MESSAGES = [
    ('meow', 'Welcome to us meow, we got free pats.'),
    ('horny', 'Welcome to our horny dungeon, hope you feeling great!.'),
    ('game', 'I hope that you brought your danmaku skills'),
]

@Sakuya.interactions(is_global=True)
async def welcome(event,
        user: ('user', 'The user to welcome'),
        message: (WELCOME_MESSAGES, 'The message to send'),
            ):
    return f'{event.user:m} welcomes {user:m} to the guild.\n{message}'


@Sakuya.interactions(guild=MY_GUILD)
async def ayaya():
    """Ayaya?"""
    return 'ayaya!'


# In this example we added only global commands. Global commands are synced only after 1 hour. But in private channels
# It is way faster. Try restarting your clients and then check private channel to the bot.

Sakuya.start()
