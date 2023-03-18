import vampytest

from ....channel import create_partial_channel_from_id, ChannelType

from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase

from ..fields import validate_target_stage
from ..preinstanced import ScheduledEventEntityType


def test__validate_target_stage__0():
    """
    Tests whether `validate_target_stage` works as intended.
    
    Case: passing.
    """
    channel_id = 202303170031
    
    for input_value, expected_output in (
        (
            None,
            (ScheduledEventEntityType.stage, ScheduledEventEntityMetadataBase(), 0),
        ), (
            channel_id,
            (ScheduledEventEntityType.stage, ScheduledEventEntityMetadataBase(), channel_id),
        ), (
            create_partial_channel_from_id(channel_id, ChannelType.guild_stage, 0),
            (ScheduledEventEntityType.stage, ScheduledEventEntityMetadataBase(), channel_id),
        ), (
            str(channel_id),
            (ScheduledEventEntityType.stage, ScheduledEventEntityMetadataBase(), channel_id),
        )
    ):
        output = validate_target_stage(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_target_stage__1():
    """
    Tests whether `validate_target_stage` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_target_stage(input_value)


def test__validate_target_stage__2():
    """
    Tests whether `validate_target_stage` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_target_stage(input_value)
