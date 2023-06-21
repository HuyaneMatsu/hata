from hata import Client, IntentFlag

TOKEN = ''

# Intents are bit flags thus bitwise operations can be used to dictate which intents are used.
# By default all gateway intents are used.
Sakuya = Client(
    TOKEN,
    intents = IntentFlag(0).update_by_keys(guilds = True, guild_messages = True)
)


@Sakuya.events
async def ready(client):
    print(f'{client:f} is connected!')


# This event will be dispatched only for guilds but not for private channels.
@Sakuya.events
async def message_create(client, message):
    print(f'Received message: {message.content!r}')


# This event will never be dispatched.
@Sakuya.events
async def user_presence_update(client, user, old_attributes):
    print('Presence Update')


Sakuya.start()
