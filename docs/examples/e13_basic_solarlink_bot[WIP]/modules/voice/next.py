from hata import Client
from hata.ext.slash import abort

from constants import TEST_GUILD
from utils import create_track_repr, get_player


Sakuya: Client

@Sakuya.interactions(guild=TEST_GUILD)
async def next_(
    client,
    event,
):
    """Plays the next song."""
    player = get_player(client, event)
    
    track = player.get_current()
    if track is None:
        abort('Nothing to skip.')
    
    
    if track.user is not event.user:
        abort('Sorry, the track was added by {event.user:m}, so only they can skip.')
    
    
    await player.skip()
    return f'Track skipped: {create_track_repr(track, None)}'
