import vampytest

from ...discovery_category import DiscoveryCategory

from ..fields import validate_sub_categories


def test__validate_sub_categories__0():
    """
    Tests whether `validate_sub_categories` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([DiscoveryCategory.gaming], (DiscoveryCategory.gaming, )),
    ):
        output = validate_sub_categories(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_sub_categories__1():
    """
    Tests whether `validate_sub_categories` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_sub_categories(input_value)
