import vampytest

from ..fields import put_sort_value


def test__put_sort_value():
    """
    Tests whether ``put_sort_value`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {'sort_value': 0}),
    ):
        data = put_sort_value(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
