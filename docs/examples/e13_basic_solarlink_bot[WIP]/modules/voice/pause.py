from hata import Client

from constants import TEST_GUILD
from utils import get_player


Sakuya: Client

@Sakuya.interactions(guild = TEST_GUILD)
async def pause(
    client,
    event,
):
    """Pauses the currently playing track."""
    player = get_player(client, event)
    
    if not player.is_paused():
        await player.pause()
    
    return 'Playing paused.'
