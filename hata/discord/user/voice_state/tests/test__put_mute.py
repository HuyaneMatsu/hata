import vampytest

from ..fields import put_mute


def test__put_mute():
    """
    Tests whether ``put_mute`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {'mute': False}),
        (False, True, {'mute': False}),
        (True, False, {'mute': True}),
    ):
        data = put_mute(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
