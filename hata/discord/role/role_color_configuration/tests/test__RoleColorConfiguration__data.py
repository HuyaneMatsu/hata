import vampytest

from ....color import Color

from ..role_color_configuration import RoleColorConfiguration

from .test__RoleColorConfiguration__constructor import _assert_fields_set


def test__RoleColorConfiguration__from_data():
    """
    Tests whether ``RoleColorConfiguration.from_data`` works as intended.
    """
    color_primary = Color(123)
    color_secondary = Color(234)
    color_tertiary = Color(345)
    
    data = {
        'primary_color': int(color_primary),
        'secondary_color': int(color_secondary),
        'tertiary_color': int(color_tertiary),
    }
    
    role_color_configuration = RoleColorConfiguration.from_data(data)
    _assert_fields_set(role_color_configuration)
    
    vampytest.assert_eq(role_color_configuration.color_primary, color_primary)
    vampytest.assert_eq(role_color_configuration.color_secondary, color_secondary)
    vampytest.assert_eq(role_color_configuration.color_tertiary, color_tertiary)


def test__RoleColorConfiguration__to_data():
    """
    Tests whether ``RoleColorConfiguration.to_data`` works as intended.
    
    Case: Include defaults.
    """
    color_primary = Color(123)
    color_secondary = Color(234)
    color_tertiary = Color(345)
    
    role_color_configuration = RoleColorConfiguration(
        color_primary = color_primary,
        color_secondary = color_secondary,
        color_tertiary = color_tertiary,
    )
    
    vampytest.assert_eq(
        role_color_configuration.to_data(
            defaults = True,
        ),
        {
            'primary_color': int(color_primary),
            'secondary_color': int(color_secondary),
            'tertiary_color': int(color_tertiary),
        },
    )
