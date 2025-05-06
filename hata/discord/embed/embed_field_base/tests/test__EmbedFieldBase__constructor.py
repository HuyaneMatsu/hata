import vampytest

from ..base import EmbedFieldBase


def _assert_fields_set(field_base):
    """
    Checks whether every fields of the given embed field are set.
    
    Parameters
    ----------
    field_base : ``EmbedFieldBase``
        The field to check.
    """
    vampytest.assert_instance(field_base, EmbedFieldBase)


def test__EmbedFieldBase__new():
    """
    Tests whether ``EmbedFieldBase.__new__`` works as intended.
    """
    field_base = EmbedFieldBase()
    _assert_fields_set(field_base)
