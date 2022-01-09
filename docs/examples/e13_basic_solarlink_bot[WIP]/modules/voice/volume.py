from hata import Client
from hata.ext.slash import P

from constants import TEST_GUILD
from utils import get_player


Sakuya: Client

@Sakuya.interactions(guild=TEST_GUILD)
async def volume_(
    client,
    event,
    volume: P('number', 'Volume percentage', min_value=0, max_value=200),
):
    """Sets the player's volume."""
    player = get_player(client, event)
    await player.set_volume(volume/100.0)
    return f'Volume set to: {volume}%.'
