import vampytest

from ..fields import put_volume_into


def test__put_volume_into():
    """
    Tests whether ``put_volume_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (1.0, False, {}),
        (0.0, False, {'volume': 0.0}),
        (1.0, True, {'volume': 1.0}),
    ):
        data = put_volume_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
