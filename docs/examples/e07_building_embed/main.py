from hata import Client, Embed, ReuAsyncIO

TOKEN = ''

Sakuya = Client(TOKEN)


@Sakuya.events
async def message_create(client, message):
    if message.content == '!hello':
        
        # This example will create a message with an embed that has a title, description, three fields and footer.
        embed = Embed(
            'This is a title',
            'This is a description',
        ).add_image(
            'attachment://flan.png'
        ).add_field(
            'This is the first field name',
            'This is a field value',
            inline=True,
        ).add_field(
            'This is the second field name',
            'Both of these fields are inline',
            inline=True,
        ).add_field(
            'This is the third field',
            'This is not an inline field',
        ).add_footer(
            'This is a footer',
        )
        
        # In this case we load image for embed from our system.
        #
        # IO operations are blocking thus loading the file asynchronously is important as blocking
        # IO takes away enough time to handle thousands of events.
        #
        # We use reusable IO as requests sometimes fail (connection issues, Discord servers derp out etc).
        # In these case the wrapper tries to repeat the request 5 times. This is when reusable io-s come to the picture.
        with (await ReuAsyncIO('flan.png')) as file:
            await client.message_create(message.channel, embed=embed, file=file)


@Sakuya.events
async def ready(client):
    print(f'{client:f} is connected!')


Sakuya.start()
