import vampytest

from ..fields import put_animated


def test__put_animated():
    """
    Tests whether ``put_animated`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'animated': False}),
        (True, False, {'animated': True}),
    ):
        data = put_animated(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
