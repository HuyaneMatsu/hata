from hata import Client

from constants import TEST_GUILD
from utils import get_player


Sakuya: Client

@Sakuya.interactions(guild=TEST_GUILD)
async def move_player(
    client,
    event,
    channel: ('channel_group_connectable', 'Select a channel.'),
):
    """Change channel of the player."""
    player = get_player(client, event)
    await player.move_to(channel)
    return f'Player moved to {channel:m}.'
