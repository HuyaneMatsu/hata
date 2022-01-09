from hata import Client

from constants import TEST_GUILD
from utils import get_player


Sakuya: Client

@Sakuya.interactions(guild=TEST_GUILD)
async def resume(
    client,
    event,
):
    """Resumes the currently playing track."""
    player = get_player(client, event)
    
    if player.is_paused():
        await player.resume()
    
    return 'Playing resumed.'
