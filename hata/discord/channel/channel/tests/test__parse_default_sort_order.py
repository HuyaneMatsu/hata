import vampytest

from ..preinstanced import SortOrder

from ..fields import parse_default_sort_order


def test__parse_default_sort_order():
    """
    Tests whether ``parse_default_sort_order`` works as intended.
    """
    for input_data, expected_output in (
        ({}, SortOrder.latest_activity),
        ({'default_sort_order': None}, SortOrder.latest_activity),
        ({'default_sort_order': SortOrder.creation_date.value}, SortOrder.creation_date),
    ):
        output = parse_default_sort_order(input_data)
        vampytest.assert_is(output, expected_output)
