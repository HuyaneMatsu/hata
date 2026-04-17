import vampytest

from ....channel import Channel

from ..fields import validate_thread


def test__validate_thread__0():
    """
    Tests whether ``validate_thread`` works as intended.
    
    Case: passing.
    """
    channel = Channel.precreate(202304300017)
    
    for input_value, expected_output in (
        (None, None),
        (channel, channel),
    ):
        output = validate_thread(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_thread__1():
    """
    Tests whether ``validate_thread`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_thread(input_value)
