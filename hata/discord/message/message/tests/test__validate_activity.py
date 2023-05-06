import vampytest

from ...message_activity import MessageActivity

from ..fields import validate_activity


def test__validate_activity__0():
    """
    Tests whether `validate_activity` works as intended.
    
    Case: passing.
    """
    activity = MessageActivity(party_id = 'Orin')
    
    for input_value, expected_output in (
        (None, None),
        (activity, activity),
    ):
        output = validate_activity(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_activity__1():
    """
    Tests whether `validate_activity` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_activity(input_value)
