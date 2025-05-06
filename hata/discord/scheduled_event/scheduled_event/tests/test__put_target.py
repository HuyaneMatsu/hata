import vampytest

from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase, ScheduledEventEntityMetadataLocation

from ..fields import put_target
from ..preinstanced import ScheduledEventEntityType


def _iter_options():
    location = 'Koishi Wonderland'
    channel_id = 202303170032
    
    yield (
        (ScheduledEventEntityType.voice, ScheduledEventEntityMetadataBase(), channel_id),
        False,
        {
            'entity_type': ScheduledEventEntityType.voice.value,
            'channel_id': str(channel_id),
        },
    )
   
    yield (
        (ScheduledEventEntityType.stage, ScheduledEventEntityMetadataBase(), channel_id),
        False,
        {
            'entity_type': ScheduledEventEntityType.stage.value,
            'channel_id': str(channel_id),
        },
    )
    
    yield (
        (ScheduledEventEntityType.location, ScheduledEventEntityMetadataLocation(location = location), 0),
        False,
        {
            'entity_type': ScheduledEventEntityType.location.value,
            'entity_metadata': ScheduledEventEntityMetadataLocation(location = location).to_data(defaults = False),
        }
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_target(input_value, defaults):
    """
    Tests whether ``put_target`` is working as intended.
    
    Parameters
    ----------
    input_value : `(ScheduledEventEntityType, ScheduledEventEntityMetadataBase, int)`
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_target(input_value, {}, defaults)
