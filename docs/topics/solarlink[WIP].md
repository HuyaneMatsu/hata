# solarlink

Solarlink is a [lavalink](https://github.com/freyacodes/Lavalink) wrapper for hata.

## Basic Startup Guide

### Start up your node

Download lavalink binaries from
[the CI server](https://ci.fredboat.com/viewLog.html?buildId=lastSuccessful&buildTypeId=Lavalink_Build&tab=artifacts&guest=1)
or from [the GitHub releases](https://github.com/freyacodes/Lavalink/releases).

Put an `application.yml` file in the lavalink binary's directory.
([Example here](https://github.com/freyacodes/Lavalink/blob/master/LavalinkServer/application.yml.example))

Run with `java -jar Lavalink.jar`

### Setup the extension and add a node

```py
from hata import Client

# Create a client with the solarlink extension
Okuu = Client(
    TOKEN,
    extensions = 'solarlink',
)

# Add a node
Okuu.solarlink.add_node('127.0.0.1', 2333, 'youshallnotpass', None)

# Parameters:
# - host
# - port
# - password
# - region
# - resume_key (optional)
# - reconnect_attempts (optional)
```

## Basic bot example


# TODO | move this to examples maybe?

```py
from hata import Client, Guild, Embed, is_url
from hata.ext.slash import abort, P

# Create client
Okuu = Client(
    TOKEN,
    extensions = ('slash', 'solarlink'),
)

# Create node
Okuu.solarlink.add_node('127.0.0.1', 2333, 'youshallnotpass', None)

# Reference the guild to add the commands to
TEST_GUILD = Guild.precreate(guild_id)


# Get player or abort the iteraction
def get_player(client, event)
    player = client.solarlink.get_player(event.guild_id)
    
    if player is None:
        abort('No player in this server!')
    
    return player

# Convert a duration to string

def duration_to_string(duration):
    duration = int(duration)
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    
    and_index = bool(hours) + bool(minutes) + bool(seconds)
    
    if and_index == 0:
        string = '0 seconds'
    
    else:
        index = 0
        string_parts = []
        for value, unit in zip(
            (hours, minutes, seconds),
            ('hours', 'minutes', 'seconds'),
        ):
            if not value:
                continue
                
            index += 1
            if index > 1:
                if index == and_index:
                    string_parts.append(' and ')
                else:
                    string_parts.append(', ')
            
            string_parts.append(str(value))
            string_parts.append(' ')
            string_parts.append(unit)
        
        string = ''.join(string_parts)
    
    return string


def create_track_repr(track, index):
    title = track.title
    if len(title) > 69:
        title = title[:66] + '...'
    
    repr_parts = []
    
    if (index is not None)
        repr_parts.append(str(index))
        repr_parts.append('.: ')
    
    repr_parts.append('[')
    repr_parts.append(title)
    repr_parts.append('](')
    repr_parts.append(track.url)
    repr_parts.append(')')
    
    return ''.join(repr_parts)


# Move player

@Okuu.interactions(guild=TEST_GUILD)
async def move_player(
    client,
    event,
    channel: ('channel_group_connectable', 'Select a channel.'),
):
    """Change channel of the player."""
    player = get_player(client, event)
    await player.move_to(channel)
    return f'Player moved to {channel:m}.'


# Move track

@Okuu.interactions(guild=TEST_GUILD)
async def move_track(
    client,
    event,
    old_position: ('int', 'The position of the track.'),
    new_position: ('int', 'The new position for the track.'),
):
    """Change position of a track"""
    player = get_player(client, event)
    
    track = payer.move_track(old_position, new_position)
    
    if track is None:
        return 'Nothing was moved.'
    
    return f'Track moved: {create_track_repr(track, None)}'


# Next

@Okuu.interactions(guild=TEST_GUILD)
async def next_(
    client,
    event,
):
    """Plays the next song."""
    player = get_player(client, event)
    
    track = player.get_current()
    if track is None:
        abort('Nothing to skip.')
    
    
    if trackuser is not event.user:
        abort('Sorry, the track was added by {event.user:m}, so only they can skip.')
    
    
    await player.skip()
    return f'Track skipped: {create_track_repr(track, None)}'


# Pause

@Okuu.interactions(guild=TEST_GUILD)
async def pause(
    client,
    event,
):
    """Pases the currently playing track."""
    player = get_player(client, event)
    
    if not player.is_paused():
        await player.pause()
    
    return 'Playing paused.'


# Play

@Okuu.interactions(guild=TEST_GUILD)
async def play(
    client,
    event,
    song_name: ('str', 'The name of the song to play'),
):
    guild = event.guild
    if (guild is None):
        abort('You need to be in a voice channel!')
    
    user = event.user
    state = guild.voice_states.get(event.user.id, None)
    if state is None:
        abort('You need to be in a voice channel!')
    
    if is_url(name):
        is_name_an_url = True
    else:
        is_name_an_url = False
        name = f'ytsearch:{name}'
    
    yield
    
    result = await client.solarlink.get_tracks(name)
    
    # No result?
    if result is None:
        track = None
    
    else:
        tracks = result.tracks
        
        # If we received a playlist, it can be empty as well
        if tracks:
            selected_track_index = result.selected_track_index
            if selected_track_index == -1:
                selected_track_index = 0
            
            track = tracks[selected_track_index]
        
        else:
            # It is empty
            track = None
    
    if track is None:
        abort('No songs found. Please try again!')
    
    player = client.solarlink.get_player(event.guild_id)
    if player is None:
        player = await client.solarlink.join_voice(state.channel)
    
    await player.append(track, user=user)
    
    yield (
        f'Track added to queue!\n'
        f'- Name: [{track.name}]({track.url}\n'
        f'- Duration: {duration_to_string(track.duration)}'
    )


# Queue

@Okuu.interactions(guild=TEST_GUILD)
async def queue(
    client,
    event,
):
    queue = player.queue
    
    embed = Embed(
        'Music queue',
        (
            f'Total number of tracks {len(queue)}\n'
            f'Total duration: {duration_to_string(player.queue_duration)}'
        ),
    )
    
    track = player.get_current()
    if (track is not None):
        embed.add_field('Currently playing', create_track_repr(track, None))
    
    if queue:
        tracks_list = [create_track_repr(repr, index) for track, index in zip(queue, range(1, 6))]
        
        queue_length = len(queue)
        if queue_length > 5:
            tracks_list.append(f'\n*{queue_length-5} not shown*')
        
        
        embed.add_field('Track list', '\n'.join(tracks_list))
    
    return embed


# Repeat

@Okuu.interactions(guild=TEST_GUILD)
async def repeat(
    client,
    event,
    option: (['track', 'queue', 'disable'], 'Repeat option'),
):
    """Set repeat for track or queue or disable both."""
    player = get_player(client, event)
    
    if option == 'track':
        player.set_repeat_current(True)
        return 'Repeating track.'
    
    if option == 'queue':
        player.set_repeat_queue(True)
        return 'Repeating queue.'
    
    player.set_repeat_current(False)
    player.set_repeat_queue(False)
    return 'Repeating disabled.'


# Resuming

@Okuu.interactions(guild=TEST_GUILD)
async def resume(
    client,
    event,
):
    """Resumes the currently playing track."""
    player = get_player(client, event)
    
    if player.is_paused():
        await player.resume()
    
    return 'Playing resumed.'

# Seeking

@Okuu.interactions(guild=TEST_GUILD)
async def seek(
    client,
    event,
    seconds: (float, 'Where to seek?'),
):
    """Seek the track."""
    player = get_player(client, event)
    
    track = player.get_current()
    if track is None:
        abort('No songs are being played right now!')
    
    duration = track.duration
    if (seconds < 0.0) or (seconds > duration):
        abort(f'Cannot seek to {seconds:.2f} seconds. Please define a value between `0` and {duration:.0f}.')
    
    await player.seek(seconds)
    return 'Seeked the current track!'

# Leaving

@Okuu.interactions(guild=TEST_GUILD)
async def leave(
    client,
    event,
):
    """Leaves me from the channel.
    player = get_player(client, event)
    await player.disconnect()
    return 'Left voice channel.'


# Setting volume

@Okuu.interactions(guild=TEST_GUILD)
async def volume_(
    client,
    event,
    volume: P('number', 'Volume percentage', min_value=0, max_value=200),
):
    """Sets the player's volume."""
    player = get_player(client, event)
    await player.set_volume(volume/100.0)
    return f'Volume set to: {volume}%.'
```
