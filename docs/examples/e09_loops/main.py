from datetime import datetime
from hata import Client, DATETIME_FORMAT_CODE, ActivityRich

TOKEN = ''

Sakuya = Client(TOKEN)


@Sakuya.events
async def ready(client):
    print(f'{client:f} is connected!')


@Sakuya.events
async def message_create(client, message):
    if message.content == '!ping':
        await client.message_create(message.channel, 'pong')


# Coroutine that changes the client presence to the current UTC time.
async def change_presence(cycler):
    activity = ActivityRich(format(datetime.utcnow(), DATETIME_FORMAT_CODE))
    await Sakuya.client_edit_presence(activity=activity)

# Cycles the given function (can be async) asynchronously. Passes itself to the function in each cycle, if you want to
# interact with the cycler.
Sakuya.loop.cycle(60.0, change_presence)


Sakuya.start()
