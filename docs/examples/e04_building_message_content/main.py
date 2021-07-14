from hata import Client

TOKEN = ''

Sakuya = Client(TOKEN)

@Sakuya.events
async def message_create(client, message):
    if message.content == '!ping':
        # To build message content, either use f strings or `str.join`. They are the best and fastest ways to build
        # strings in python.
        
        # Discord messages support markdown formatting.
        
        content = f'User **{message.author.name}** used the \'ping\' command in the {message.channel.mention} channel'
        
        # In format strings you can use format codes for entities as well.
        # `{user.name}` can be replaced just by `{user}`, or `{channel.mention}` by `{channel:m}`.
        
        await client.message_create(message.channel, content)

@Sakuya.events
async def ready(client):
    print(f'{client:f} is connected!')


Sakuya.start()
