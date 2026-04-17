import vampytest

from ....channel import Channel

from ..fields import validate_safety_alerts_channel_id


def test__validate_safety_alerts_channel_id__0():
    """
    Tests whether `validate_safety_alerts_channel_id` works as intended.
    
    Case: passing.
    """
    safety_alerts_channel_id = 202301150018
    
    for input_value, expected_output in (
        (None, 0),
        (safety_alerts_channel_id, safety_alerts_channel_id),
        (Channel.precreate(safety_alerts_channel_id), safety_alerts_channel_id),
        (str(safety_alerts_channel_id), safety_alerts_channel_id)
    ):
        output = validate_safety_alerts_channel_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_safety_alerts_channel_id__1():
    """
    Tests whether `validate_safety_alerts_channel_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '-1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_safety_alerts_channel_id(input_value)


def test__validate_safety_alerts_channel_id__2():
    """
    Tests whether `validate_safety_alerts_channel_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_safety_alerts_channel_id(input_value)
