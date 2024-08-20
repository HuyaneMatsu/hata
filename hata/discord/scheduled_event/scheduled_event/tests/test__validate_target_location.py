import vampytest

from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataLocation

from ..fields import validate_target_location
from ..preinstanced import ScheduledEventEntityType


def _iter_options__passing():
    location = 'hell'
    
    yield (
        None,
        (
            ScheduledEventEntityType.location,
            ScheduledEventEntityMetadataLocation(),
            0,
        ),
    )
    
    yield (
        location,
        (
            ScheduledEventEntityType.location,
            ScheduledEventEntityMetadataLocation(location = location),
            0,
        ),
    )
    
    yield (
        '',
        (
            ScheduledEventEntityType.location,
            ScheduledEventEntityMetadataLocation(),
            0,
        ),
    )


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_target_location(input_value):
    """
    Tests whether `validate_target_location` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    entity_type : ``ScheduledEventEntityType``
        Scheduled event entity type.
    entity_metadata : ``ScheduledEventEntityMetadataBase``
        Scheduled event entity metadata.
    channel_id : `int`
        Scheduled event target channel identifier.
    
    Raises
    ------
    TypeError
    """
    output = validate_target_location(input_value)
    vampytest.assert_instance(output, tuple)
    return output
