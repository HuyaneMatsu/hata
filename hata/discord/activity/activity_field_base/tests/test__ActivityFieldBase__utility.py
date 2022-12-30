import vampytest

from ..base import ActivityFieldBase

from .test__ActivityFieldBase__constructor import _check_fields_set


def test__ActivityFieldBase__copy():
    """
    Tests whether ``ActivityFieldBase.copy`` works as intended.
    """
    field = ActivityFieldBase()
    copy = field.copy()
    _check_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__ActivityFieldBase__copy_with__0():
    """
    Tests whether ``ActivityFieldBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    field = ActivityFieldBase()
    copy = field.copy_with()
    _check_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)
