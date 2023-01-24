import vampytest

from ..fields import put_mute_into


def test__put_mute_into():
    """
    Tests whether ``put_mute_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {'mute': False}),
        (False, True, {'mute': False}),
        (True, False, {'mute': True}),
    ):
        data = put_mute_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
