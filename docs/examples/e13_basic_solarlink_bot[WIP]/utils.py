# Shared functionality used by multiple commands
# If too crowded, you might want to crate a separate directory for it.

from hata.ext.slash import abort


# Get player or abort the interaction
def get_player(client, event):
    player = client.solarlink.get_player(event.guild_id)
    
    if player is None:
        abort('No player in this server!')
    
    return player


# Convert a duration to string
def duration_to_string(duration):
    duration = int(duration)
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    
    and_index = bool(hours) + bool(minutes) + bool(seconds)
    
    if and_index == 0:
        string = '0 seconds'
    
    else:
        index = 0
        string_parts = []
        for value, unit in zip(
            (hours, minutes, seconds),
            ('hours', 'minutes', 'seconds'),
        ):
            if not value:
                continue
                
            index += 1
            if index > 1:
                if index == and_index:
                    string_parts.append(' and ')
                else:
                    string_parts.append(', ')
            
            string_parts.append(str(value))
            string_parts.append(' ')
            string_parts.append(unit)
        
        string = ''.join(string_parts)
    
    return string


# Creates track short representation.
def create_track_repr(track, index):
    title = track.title
    if len(title) > 69:
        title = title[:66] + '...'
    
    repr_parts = []
    
    if (index is not None):
        repr_parts.append(str(index))
        repr_parts.append('.: ')
    
    repr_parts.append('[')
    repr_parts.append(title)
    repr_parts.append('](')
    repr_parts.append(track.url)
    repr_parts.append(')')
    
    return ''.join(repr_parts)


# Gets player queue duration
def get_queue_duration(player):
    duration = 0.0
    
    for configured_track in player.queue:
        duration += configured_track.track.duration
    
    return duration
