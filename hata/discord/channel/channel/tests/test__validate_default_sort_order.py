import vampytest

from ..fields import validate_default_sort_order
from ..preinstanced import SortOrder


def test__validate_default_sort_order__0():
    """
    Validates whether ``validate_default_sort_order`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, SortOrder.latest_activity),
        (SortOrder.creation_date, SortOrder.creation_date),
        (SortOrder.creation_date.value, SortOrder.creation_date)
    ):
        output = validate_default_sort_order(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_default_sort_order__1():
    """
    Validates whether ``validate_default_sort_order`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_default_sort_order(input_value)
