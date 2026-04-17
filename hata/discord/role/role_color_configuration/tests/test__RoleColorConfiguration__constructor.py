import vampytest

from ....color import Color

from ..role_color_configuration import RoleColorConfiguration


def _assert_fields_set(role_color_configuration):
    """
    Asserts whether all fields of the given role color configuration are set.
    
    Parameters
    ----------
    role_color_configuration : ``RoleColorConfiguration``
    """
    vampytest.assert_instance(role_color_configuration, RoleColorConfiguration)
    vampytest.assert_instance(role_color_configuration.color_primary, Color)
    vampytest.assert_instance(role_color_configuration.color_secondary, Color, nullable = True)
    vampytest.assert_instance(role_color_configuration.color_tertiary, Color, nullable = True)


def test__RoleColorConfiguration__new__no_fields():
    """
    Tests whether ``RoleColorConfiguration.__new__`` works as intended.
    
    Case: No parameters.
    """
    role_color_configuration = RoleColorConfiguration()
    _assert_fields_set(role_color_configuration)


def test__RoleColorConfiguration__new__all_fields():
    """
    Tests whether ``RoleColorConfiguration.__new__`` works as intended.
    
    Case: all fields.
    """
    color_primary = Color(123)
    color_secondary = Color(234)
    color_tertiary = Color(345)
    
    role_color_configuration = RoleColorConfiguration(
        color_primary = color_primary,
        color_secondary = color_secondary,
        color_tertiary = color_tertiary,
    )
    _assert_fields_set(role_color_configuration)
    
    vampytest.assert_eq(role_color_configuration.color_primary, color_primary)
    vampytest.assert_eq(role_color_configuration.color_secondary, color_secondary)
    vampytest.assert_eq(role_color_configuration.color_tertiary, color_tertiary)


def test__RoleColorConfiguration__create_empty():
    """
    Tests whether ``RoleColorConfiguration.create_empty`` works as intended.
    """
    role_color_configuration = RoleColorConfiguration.create_empty()
    _assert_fields_set(role_color_configuration)


def test__RoleColorConfiguration__create_from_color_primary():
    """
    Tests whether ``RoleColorConfiguration.create_from_color_primary`` works as intended.
    """
    color_primary = Color(123)
    
    role_color_configuration = RoleColorConfiguration.create_from_color_primary(color_primary)
    _assert_fields_set(role_color_configuration)
    
    vampytest.assert_eq(role_color_configuration.color_primary, color_primary)
