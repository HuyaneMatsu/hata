from hata import Client

from constants import TEST_GUILD
from utils import create_track_repr, get_player


Sakuya: Client

@Sakuya.interactions(guild = TEST_GUILD)
async def move_track(
    client,
    event,
    old_position: ('int', 'The position of the track.'),
    new_position: ('int', 'The new position for the track.'),
):
    """Change position of a track."""
    player = get_player(client, event)
    
    track = player.move_track(old_position, new_position)
    
    if track is None:
        return 'Nothing was moved.'
    
    return f'Track moved: {create_track_repr(track, None)}'
