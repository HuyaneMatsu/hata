import vampytest

from .. import ActivityFieldBase


def test__ActivityFieldBase__new():
    """
    Tests whether ``ActivityFieldBase.__new__`` works as intended.
    """
    field = ActivityFieldBase()
    vampytest.assert_instance(field, ActivityFieldBase)
