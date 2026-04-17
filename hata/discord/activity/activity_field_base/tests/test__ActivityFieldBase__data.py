import vampytest

from ..base import ActivityFieldBase

from .test__ActivityFieldBase__constructor import _assert_fields_set


def test__ActivityFieldBase__from_data():
    """
    Tests whether ``ActivityFieldBase.from_data`` works as intended.
    """
    field = ActivityFieldBase.from_data({})
    _assert_fields_set(field)


def test__ActivityFieldBase__to_data():
    """
    Tests whether ``ActivityFieldBase.from_data`` works as intended.
    """
    field = ActivityFieldBase()
    
    data = field.to_data()
    
    vampytest.assert_eq(data, {})
