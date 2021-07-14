from hata import Client, IntentFlag

TOKEN = ''

# Intents are a bit flags, bitwise operations can be used to dictate which intents to use
# By default all gateway intent is used.
Sakuya = Client(TOKEN,
    intents = IntentFlag().update_by_keys(guilds=True, guild_messages=True)
)


@Sakuya.events
async def ready(client):
    print(f'{client:f} is connected!')


# This event will be dispatched only for guilds, but not for private channels.
@Sakuya.clients
async def message(client, message):
    print(f'Received message: {message.content!r}')


# This event will be never dispatched.
@Sakuya.events
async def user_presence_update(client, user, old_attributes):
    print('Presence Update')


Sakuya.start()
