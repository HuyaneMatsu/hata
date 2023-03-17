import vampytest

from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase, ScheduledEventEntityMetadataLocation

from ..fields import parse_entity_metadata
from ..preinstanced import ScheduledEventEntityType


def test__parse_entity_metadata():
    """
    Tests whether ``parse_entity_metadata`` is working as intended.
    """
    entity_metadata = ScheduledEventEntityMetadataLocation({'location': 'Koishi Wonderland'})
    
    for input_data, entity_metadata_type, expected_output in (
        ({}, ScheduledEventEntityType.none, ScheduledEventEntityMetadataBase({})),
        ({'entity_metadata': None}, ScheduledEventEntityType.location, ScheduledEventEntityMetadataLocation({})),
        (
            {'entity_metadata': entity_metadata.to_data(defaults = False)},
            ScheduledEventEntityType.location, entity_metadata,
        ),
    ):
        entity_metadata = parse_entity_metadata(input_data, entity_metadata_type)
        vampytest.assert_eq(entity_metadata, expected_output)
