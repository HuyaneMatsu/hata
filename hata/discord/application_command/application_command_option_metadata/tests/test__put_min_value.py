import vampytest

from ..fields import put_min_value


def test__put_min_value():
    """
    Tests whether ``put_min_value`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'min_value': None}),
        (0, False, {'min_value': 0}),
        (0.0, False, {'min_value': 0.0}),
    ):
        data = put_min_value(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
