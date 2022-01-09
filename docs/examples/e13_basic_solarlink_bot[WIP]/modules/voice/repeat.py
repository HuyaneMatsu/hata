from hata import Client, Embed

from constants import TEST_GUILD
from utils import get_player


Sakuya: Client


@Sakuya.interactions(guild=TEST_GUILD)
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
