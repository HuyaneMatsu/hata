# This example shows basic interaction with voice channels.
# We can join `VoiceClient`-s to them and play or capture audio.
#
# We're using `commands_v2` extension since it provides an easy API to access user voice state or the local voice client
#
# The example will showcase the following actions:
# => Connecting to voice channel.
# => Changing volume.
# => Playing audio from youtube.
# => Disconnecting.

from hata import Client, YTAudio, DownloadError, Guild

TOKEN = ''


Sakuya = Client(
    TOKEN,
    extensions = 'slash',
)


@Sakuya.events
async def ready(client):
    print(f'{client:f} is connected!')

MY_GUILD = Guild.precreate(12345)


@Sakuya.interactions(guild=MY_GUILD)
async def join(client, event):
    """Joins to voice channel."""
    # Getting the author voice state
    voice_state = event.voice_state
    if voice_state is None:
        return 'You are not at a voice channel!'
    
    # Connecting the client to the same channel, where the user is.
    try:
        await client.join_voice(voice_state.channel)
    except TimeoutError:
        # Could not connect.
        return 'Timed out meanwhile tried to connect.'
    
    except RuntimeError:
        # Not every required library is installed.
        return 'The client cannot play voice, some libraries are not loaded.'
    
    # Great success.
    return f'Joined to {voice_state.channel.name}'


@Sakuya.interactions(guild=MY_GUILD)
async def yt(event,
    url: ('str', 'The name or the url of a track') = None,
):
    """Plays from youtube."""
    # Checking whether `youtube_dl` is installed.
    if YTAudio is None:
        return 'This option in unavailable :c'
    
    if url is None:
        return 'Please define what to play.'
    
    voice_client = event.voice_client
    if voice_client is None:
        return 'There is no voice client at your guild.'

    try:
        source = await YTAudio(url, stream=True)
    except DownloadError:
        # Raised by `youtube_dl` if downloading failed.
        return 'Error meanwhile downloading'
    
    # Appending to the voice clients queue either returns `True` (if the audio just started to play) or `False` (if the
    # voice client has anything in its queue).
    if voice_client.append(source):
        content = 'Now playing'
    else:
        content = 'Added to queue'
    
    return f'{content} {source.title}!'


# Tailing `_` are removed from command names.
@Sakuya.interactions(guild=MY_GUILD)
async def volume_(event,
    volume: ('int', 'Volume to set to.') = None,
):
    """Changes the player\'s volume."""
    voice_client = event.voice_client
    if voice_client is None:
        return 'There is no voice client at your guild.'
    
    if volume is None:
        return f'{voice_client.volume * 100.:.0f}%'
    
    # Volume can be between 0.0 and 2.0, but it is more natural to ask for percentage
    if volume <= 0:
        volume = 0.0
    elif volume >= 200:
        volume = 2.0
    else:
        volume /= 100.0
    
    voice_client.volume = volume
    return f'Volume set to {volume * 100.:.0f}%'


@Sakuya.interactions(guild=MY_GUILD)
async def disconnect(event):
    """Disconnects the bot from voice."""
    voice_client = event.voice_client
    if voice_client is None:
        return 'There is no voice client at your guild.'
    
    await voice_client.disconnect()
    return 'Disconnected.'

Sakuya.start()
