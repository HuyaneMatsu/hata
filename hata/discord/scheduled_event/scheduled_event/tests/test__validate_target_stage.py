import vampytest

from ....channel import create_partial_channel_from_id, ChannelType

from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase

from ..fields import validate_target_stage
from ..preinstanced import ScheduledEventEntityType


def _iter_options__passing():
    channel_id = 202303170031
    
    yield (
        None,
        (
            ScheduledEventEntityType.stage,
            ScheduledEventEntityMetadataBase(),
            0,
        ),
    )
           
    yield (
        channel_id,
        (
            ScheduledEventEntityType.stage,
            ScheduledEventEntityMetadataBase(),
            channel_id,
        ),
    )
    
    yield(
        create_partial_channel_from_id(channel_id, ChannelType.guild_stage, 0),
        (
            ScheduledEventEntityType.stage,
            ScheduledEventEntityMetadataBase(),
            channel_id,
        ),
    )
    
    yield (
        str(channel_id),
        (
            ScheduledEventEntityType.stage,
            ScheduledEventEntityMetadataBase(),
            channel_id,
        ),
    )


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield '-1'
    yield -1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_target_stage(input_value):
    """
    Tests whether `validate_target_stage` works as intended.
    
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
    ValueError
    """
    output = validate_target_stage(input_value)
    vampytest.assert_instance(output, tuple)
    return output
