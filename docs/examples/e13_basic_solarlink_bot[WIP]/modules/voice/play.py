from hata import Client, is_url
from hata.ext.slash import abort

from constants import TEST_GUILD
from utils import duration_to_string


Sakuya: Client

@Sakuya.interactions(guild = TEST_GUILD)
async def play(
    client,
    event,
    song_name: ('str', 'The name of the song to play'),
):
    """Play a song."""
    guild = event.guild
    if (guild is None):
        abort('You need to be in a voice channel!')
    
    user = event.user
    state = guild.get_voice_state(event.user.id)
    if state is None:
        abort('You need to be in a voice channel!')
    
    if not is_url(song_name):
        song_name = f'ytsearch:{song_name}'
    
    yield
    
    result = await client.solarlink.get_tracks(song_name)
    
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
    
    await player.append(track, user = user)
    
    yield (
        f'Track added to queue!\n'
        f'- Name: [{track.title}]({track.url})\n'
        f'- Duration: {duration_to_string(track.duration)}'
    )
