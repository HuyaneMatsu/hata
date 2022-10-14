import vampytest

from ...channel import Channel

from ..parent_id import validate_parent_id


def test__validate_parent_id__0():
    """
    Tests whether `validate_parent_id` works as intended.
    
    Case: passing.
    """
    channel_id = 202209130000
    
    for input_value, expected_output in (
        (None, 0),
        (channel_id, channel_id),
        (Channel.precreate(channel_id), channel_id),
        (str(channel_id), channel_id)
    ):
        output = validate_parent_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_parent_id__1():
    """
    Tests whether `validate_parent_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_parent_id(input_value)


def test__validate_parent_id__2():
    """
    Tests whether `validate_parent_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_parent_id(input_value)
