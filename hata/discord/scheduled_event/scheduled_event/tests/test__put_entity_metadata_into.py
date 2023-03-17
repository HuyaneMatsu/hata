import vampytest

from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase, ScheduledEventEntityMetadataLocation

from ..fields import put_entity_metadata_into


def test__put_entity_metadata_into():
    """
    Tests whether ``put_entity_metadata_into`` is working as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataLocation({'location': 'Koishi Wonderland'})
    
    for input_value, defaults, expected_output in (
        (ScheduledEventEntityMetadataBase({}), False, {}),
        (ScheduledEventEntityMetadataBase({}), True, {'entity_metadata': {}}),
        (entity_metadata, False, {'entity_metadata': entity_metadata.to_data(defaults = False)}),
    ):
        data = put_entity_metadata_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
