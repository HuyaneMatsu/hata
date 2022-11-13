from hata import Client
from hata.ext.slash import abort

from constants import TEST_GUILD
from utils import get_player


Sakuya: Client

@Sakuya.interactions(guild = TEST_GUILD)
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
