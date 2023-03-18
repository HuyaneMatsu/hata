import vampytest

from ....channel import create_partial_channel_from_id, ChannelType

from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase

from ..fields import validate_target_voice
from ..preinstanced import ScheduledEventEntityType


def test__validate_target_voice__0():
    """
    Tests whether `validate_target_voice` works as intended.
    
    Case: passing.
    """
    channel_id = 202303170033
    
    for input_value, expected_output in (
        (
            None,
            (ScheduledEventEntityType.voice, ScheduledEventEntityMetadataBase(), 0),
        ), (
            channel_id,
            (ScheduledEventEntityType.voice, ScheduledEventEntityMetadataBase(), channel_id),
        ), (
            create_partial_channel_from_id(channel_id, ChannelType.guild_voice, 0),
            (ScheduledEventEntityType.voice, ScheduledEventEntityMetadataBase(), channel_id),
        ), (
            str(channel_id),
            (ScheduledEventEntityType.voice, ScheduledEventEntityMetadataBase(), channel_id),
        )
    ):
        output = validate_target_voice(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_target_voice__1():
    """
    Tests whether `validate_target_voice` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_target_voice(input_value)


def test__validate_target_voice__2():
    """
    Tests whether `validate_target_voice` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_target_voice(input_value)
