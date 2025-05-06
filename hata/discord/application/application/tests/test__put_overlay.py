import vampytest

from ..fields import put_overlay


def test__put_overlay():
    """
    Tests whether ``put_overlay`` works as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'overlay': False}),
        (True, False, {'overlay': True}),
    ):
        data = put_overlay(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
