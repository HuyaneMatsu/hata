import vampytest

from ..fields import put_primary


def test__put_primary():
    """
    Tests whether ``put_primary`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'is_primary': False}),
        (True, False, {'is_primary': True}),
    ):
        data = put_primary(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
