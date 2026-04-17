import vampytest

from ..base import ActivityFieldBase


def test__ActivityFieldBase__repr():
    """
    Tests whether ``ActivityFieldBase.__repr__`` works as intended.
    """
    field = ActivityFieldBase()
    vampytest.assert_instance(repr(field), str)


def test__ActivityFieldBase__hash():
    """
    Tests whether ``ActivityFieldBase.__hash__`` works as intended.
    """
    field = ActivityFieldBase()
    vampytest.assert_instance(hash(field), int)


def test__ActivityFieldBase__eq():
    """
    Tests whether ``ActivityFieldBase.__eq__`` works as intended.
    """
    field = ActivityFieldBase()
    vampytest.assert_eq(field, field)
    vampytest.assert_ne(field, object())
