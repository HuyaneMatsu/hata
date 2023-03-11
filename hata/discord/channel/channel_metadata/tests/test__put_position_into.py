import vampytest

from ..fields import put_position_into


def test__put_position_into():
    """
    Tests whether ``put_position_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {'position': 0}),
    ):
        data = put_position_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
