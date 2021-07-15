from hata import Client, Guild, YTAudio, DownloadError
from hata.ext.commands_v2 import checks

TOKEN = ''

Sakuya = Client(TOKEN,
    extensions = 'commands_v2',
    prefix = '!',
)

@Sakuya.events
async def ready(client):
    print(f'{client:f} is connected!')


@Sakuya.commands
@checks.guild_only()
async def join(ctx):
    """Joins to voice channel."""
    # Getting the author's voice state
    voice_state = ctx.voice_state
    if voice_state is None:
        return 'You are not at a voice channel!'
    
    # Connecting the client to the same channel, where the user is.
    try:
        await ctx.client.join_voice(voice_state.channel)
    except TimeoutError:
        # Could not connect.
        return 'Timed out meanwhile tried to connect.'
    
    except RuntimeError:
        # Not every library is installed.
        return 'The client cannot play voice, some libraries are not loaded.'
    
    # Great success.
    return f'Joined to {voice_state.channel.name}'


@Sakuya.commands
@checks.guild_only()
async def yt(ctx, url=None):
    """Plays from youtube."""
    # Checking whether `youtube_dl` is installed.
    if YTAudio is None:
        return 'This option in unavailable :c'
    
    if url is None:
        return 'Please define what to play.'
    
    voice_client = ctx.voice_client
    if voice_client is None:
        return 'There is no voice client at your guild.'

    try:
        source = await YTAudio(url, stream=True)
    except DownloadError:
        # Raised by `youtube_dl` if downloading failed.
        return 'Error meanwhile downloading'
    
    # Appending a voice client's queue either returns `True`, if the audio just started to play, or `False`, if the
    # voice client has anything on it's queue.
    if voice_client.append(source):
        content = 'Now playing'
    else:
        content = 'Added to queue'
    
    return f'{content} {source.title}!'


# Tailing `_` are removed from command names.
@Sakuya.commands
@checks.guild_only()
async def volume_(ctx, volume:int=None):
    """Changes the player\'s volume."""
    voice_client = ctx.voice_client
    if voice_client is None:
        return 'There is no voice client at your guild.'
    
    if volume is None:
        return f'{voice_client.volume*100.:.0f}%'
    
    # Volume can be between 0.0 and 2.0, but it is more natural to ask for percentage
    if volume <= 0:
        volume = 0.0
    elif volume >= 200:
        volume = 2.0
    else:
        volume /= 100.0
    
    voice_client.volume = volume
    return f'Volume set to {volume}%'


@Sakuya.commands
@checks.guild_only()
async def disconnect(ctx):
    """Disconnects the bot from voice."""
    voice_client = ctx.voice_client
    if voice_client is None:
        return 'There is no voice client at your guild.'
    
    await voice_client.disconnect()


Sakuya.start()
