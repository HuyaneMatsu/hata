import vampytest

from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase, ScheduledEventEntityMetadataLocation

from ..fields import parse_entity_metadata
from ..preinstanced import ScheduledEventEntityType


def _iter_options():
    entity_metadata = ScheduledEventEntityMetadataLocation(location = 'Koishi Wonderland')
    
    yield (
        {},
        ScheduledEventEntityType.none,
        ScheduledEventEntityMetadataBase(),
    )
    
    yield (
        {'entity_metadata': None},
        ScheduledEventEntityType.location,
        ScheduledEventEntityMetadataLocation(),
    )
    
    yield (
        {'entity_metadata': entity_metadata.to_data(defaults = False)},
        ScheduledEventEntityType.location,
        entity_metadata,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_entity_metadata(input_data, entity_metadata_type):
    """
    Tests whether ``parse_entity_metadata`` is working as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    entity_metadata_type : ``ScheduledEventEntityType``
        Entity metadata type.
    
    Returns
    -------
    output : ``ScheduledEventEntityMetadataBase``
    """
    output = parse_entity_metadata(input_data, entity_metadata_type)
    vampytest.assert_instance(output, ScheduledEventEntityMetadataBase)
    return output
