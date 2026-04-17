import vampytest

from ....channel import Channel

from ..fields import validate_rules_channel_id


def test__validate_rules_channel_id__0():
    """
    Tests whether `validate_rules_channel_id` works as intended.
    
    Case: passing.
    """
    rules_channel_id = 202306100011
    
    for input_value, expected_output in (
        (None, 0),
        (rules_channel_id, rules_channel_id),
        (Channel.precreate(rules_channel_id), rules_channel_id),
        (str(rules_channel_id), rules_channel_id)
    ):
        output = validate_rules_channel_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_rules_channel_id__1():
    """
    Tests whether `validate_rules_channel_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '-1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_rules_channel_id(input_value)


def test__validate_rules_channel_id__2():
    """
    Tests whether `validate_rules_channel_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_rules_channel_id(input_value)
