import vampytest

from ..base import ActivityFieldBase


def _check_fields_set(field):
    """
    Checks whether every fields of the given activity field are set.
    
    Parameters
    ----------
    field : ``ActivityFieldBase``
        The field to check.
    """
    vampytest.assert_instance(field, ActivityFieldBase)


def test__ActivityFieldBase__new():
    """
    Tests whether ``ActivityFieldBase.__new__`` works as intended.
    """
    field = ActivityFieldBase()
    _check_fields_set(field)
