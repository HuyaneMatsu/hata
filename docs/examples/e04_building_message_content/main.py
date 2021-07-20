from hata import Client

TOKEN = ''

Sakuya = Client(TOKEN)


@Sakuya.events
async def message_create(client, message):
    if message.content == '!ping':
        # To build message content we just build a regular Python string. Here we used Python f string.
        # Note that Discord messages support markdown formatting, so here for example we used ** which marks
        # text as bold for anything in between it
        content = f'User **{message.author.name}** used the \'ping\' command in the {message.channel.mention} channel.'
        # In format strings you can use format codes for entities as well.
        # `{user.name}` can be replaced just by `{user}`, or `{channel.mention}` by `{channel:m}`.

        # We send constructed string to the channel where '!ping' was called
        await client.message_create(message.channel, content)


@Sakuya.events
async def ready(client):
    print(f'{client:f} is connected!')


Sakuya.start()
