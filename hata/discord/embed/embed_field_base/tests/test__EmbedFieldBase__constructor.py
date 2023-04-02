import vampytest

from ..base import EmbedFieldBase


def _assert_fields_set(field):
    """
    Checks whether every fields of the given activity field are set.
    
    Parameters
    ----------
    field : ``EmbedFieldBase``
        The field to check.
    """
    vampytest.assert_instance(field, EmbedFieldBase)


def test__EmbedFieldBase__new():
    """
    Tests whether ``EmbedFieldBase.__new__`` works as intended.
    """
    field = EmbedFieldBase()
    _assert_fields_set(field)
