import vampytest

from .. import ActivityFieldBase


def test__ActivityFieldBase__from_data():
    """
    Tests whether ``ActivityFieldBase.from_data`` works as intended.
    """
    field = ActivityFieldBase.from_data({})
    vampytest.assert_instance(field, ActivityFieldBase)


def test__ActivityFieldBase__to_data():
    """
    Tests whether ``ActivityFieldBase.from_data`` works as intended.
    """
    field = ActivityFieldBase()
    
    data = field.to_data()
    
    vampytest.assert_eq(data, {})
