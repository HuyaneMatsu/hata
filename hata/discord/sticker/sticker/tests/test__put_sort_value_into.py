import vampytest

from ..fields import put_sort_value_into


def test__put_sort_value_into():
    """
    Tests whether ``put_sort_value_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {'sort_value': 0}),
    ):
        data = put_sort_value_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
