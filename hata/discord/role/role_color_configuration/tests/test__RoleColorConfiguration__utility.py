import vampytest

from ....color import Color

from ..role_color_configuration import RoleColorConfiguration

from .test__RoleColorConfiguration__constructor import _assert_fields_set


def test__RoleColorConfiguration__copy():
    """
    Tests whether ``RoleColorConfiguration.copy`` works as intended.
    """
    color_primary = Color(123)
    color_secondary = Color(234)
    color_tertiary = Color(345)
    
    role_color_configuration = RoleColorConfiguration(
        color_primary = color_primary,
        color_secondary = color_secondary,
        color_tertiary = color_tertiary,
    )
    copy = role_color_configuration.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(role_color_configuration, copy)
    vampytest.assert_eq(role_color_configuration, copy)


def test__RoleColorConfiguration__copy_with__no_fields():
    """
    Tests whether ``RoleColorConfiguration.copy_with`` works as intended.
    
    Case: No fields given.
    """
    color_primary = Color(123)
    color_secondary = Color(234)
    color_tertiary = Color(345)
    
    role_color_configuration = RoleColorConfiguration(
        color_primary = color_primary,
        color_secondary = color_secondary,
        color_tertiary = color_tertiary,
    )
    copy = role_color_configuration.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(role_color_configuration, copy)
    vampytest.assert_eq(role_color_configuration, copy)


def test__RoleColorConfiguration__copy_with__all_fields():
    """
    Tests whether ``RoleColorConfiguration.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_color_primary = Color(123)
    old_color_secondary = Color(234)
    old_color_tertiary = Color(345)
    
    new_color_primary = Color(123)
    new_color_secondary = Color(234)
    new_color_tertiary = Color(345)
    
    role_color_configuration = RoleColorConfiguration(
        color_primary = old_color_primary,
        color_secondary = old_color_secondary,
        color_tertiary = old_color_tertiary,
    )
    copy = role_color_configuration.copy_with(
        color_primary = new_color_primary,
        color_secondary = new_color_secondary,
        color_tertiary = new_color_tertiary,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(role_color_configuration, copy)

    vampytest.assert_eq(copy.color_primary, new_color_primary)
    vampytest.assert_eq(copy.color_secondary, new_color_secondary)
    vampytest.assert_eq(copy.color_tertiary, new_color_tertiary)
