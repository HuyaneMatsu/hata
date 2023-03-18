import vampytest

from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase, ScheduledEventEntityMetadataLocation

from ..fields import put_target_into
from ..preinstanced import ScheduledEventEntityType


def test__put_target_into():
    """
    Tests whether ``put_target_into`` is working as intended.
    """
    location = 'Koishi Wonderland'
    channel_id = 202303170032
    
    for input_value, defaults, expected_output in (
        (
            (ScheduledEventEntityType.voice, ScheduledEventEntityMetadataBase(), channel_id),
            False,
            {
                'entity_type': ScheduledEventEntityType.voice.value,
                'channel_id': str(channel_id),
            },
        ), (
            (ScheduledEventEntityType.stage, ScheduledEventEntityMetadataBase(), channel_id),
            False,
            {
                'entity_type': ScheduledEventEntityType.stage.value,
                'channel_id': str(channel_id),
            },
        ), (
            (ScheduledEventEntityType.location, ScheduledEventEntityMetadataLocation(location = location), 0),
            False,
            {
                'entity_type': ScheduledEventEntityType.location.value,
                'entity_metadata': ScheduledEventEntityMetadataLocation(location = location).to_data(defaults = False),
            }
        ),
    ):
        data = put_target_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
