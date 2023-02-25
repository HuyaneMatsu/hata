import vampytest

from ..fields import put_max_value_into


def test__put_max_value_into():
    """
    Tests whether ``put_max_value_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'max_value': None}),
        (0, False, {'max_value': 0}),
        (0.0, False, {'max_value': 0.0}),
    ):
        data = put_max_value_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
