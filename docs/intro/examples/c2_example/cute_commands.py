from hata import eventlist, BUILTIN_EMOJIS

CAKE = BUILTIN_EMOJIS['cake']

cute_commands = eventlist()

@cute_commands
async def cake(client, message):
    await client.message_create(message.channel, CAKE.as_emoji)

@cute_commands(name='love')
async def send_love(client, message):
    channel = await client.channel_private_create(message.author)
    await client.message_create(channel, 'I love you :3')
