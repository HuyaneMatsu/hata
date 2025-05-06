import vampytest

from ..fields import put_large


def test__put_large():
    """
    Tests whether ``put_large`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'large': False}),
        (True, False, {'large': True}),
    ):
        data = put_large(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
