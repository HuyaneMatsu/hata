import vampytest

from ...discovery_category import DiscoveryCategory

from ..fields import validate_primary_category


def test__validate_primary_category__0():
    """
    Validates whether ``validate_primary_category`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, DiscoveryCategory.general),
        (DiscoveryCategory.gaming, DiscoveryCategory.gaming),
        (DiscoveryCategory.gaming.value, DiscoveryCategory.gaming),
    ):
        output = validate_primary_category(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_primary_category__1():
    """
    Validates whether ``validate_primary_category`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_primary_category(input_value)
