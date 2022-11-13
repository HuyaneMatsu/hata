from hata import Client, Embed

from constants import TEST_GUILD
from utils import duration_to_string, get_queue_duration, create_track_repr


Sakuya: Client


@Sakuya.interactions(guild = TEST_GUILD)
async def queue_(
    client,
    event,
):
    player = client.solarlink.get_player(event.guild_id)
    
    queue = player.queue
    
    embed = Embed(
        'Music queue',
        (
            f'Total number of tracks {len(queue)}\n'
            f'Total duration: {duration_to_string(get_queue_duration(player))}'
        ),
    )
    
    track = player.get_current()
    if (track is not None):
        embed.add_field('Currently playing', create_track_repr(track, None))
    
    if queue:
        tracks_list = [create_track_repr(repr, index) for track, index in zip(queue, range(1, 6))]
        
        queue_length = len(queue)
        if queue_length > 5:
            tracks_list.append(f'\n*{queue_length-5} not shown*')
        
        
        embed.add_field('Track list', '\n'.join(tracks_list))
    
    return embed
