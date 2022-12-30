import vampytest

from ..fields import put_size_and_max_into


def test__put_size_and_max_into():
    """
    Tests whether ``put_size_and_max_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        ((0, 0), False, {}),
        ((0, 0), True, {'size': (0, 0)}),
        ((10, 20), False, {'size': (10, 20)}),
    ):
        output = put_size_and_max_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
