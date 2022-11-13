from hata import Client

from constants import TEST_GUILD
from utils import get_player


Sakuya: Client

@Sakuya.interactions(guild = TEST_GUILD)
async def leave(
    client,
    event,
):
    """Leaves me from the channel."""
    player = get_player(client, event)
    await player.disconnect()
    return 'Left voice channel.'
