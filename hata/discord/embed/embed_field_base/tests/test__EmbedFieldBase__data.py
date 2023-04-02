import vampytest

from ..base import EmbedFieldBase

from .test__EmbedFieldBase__constructor import _assert_fields_set



def test__EmbedFieldBase__from_data():
    """
    Tests whether ``EmbedFieldBase.from_data`` works as intended.
    """
    data = {}
    
    field = EmbedFieldBase.from_data(data)
    _assert_fields_set(field)


def test__EmbedFieldBase__to_data():
    """
    Tests whether ``EmbedFieldBase.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    field = EmbedFieldBase()
    
    expected_output = {}
    
    vampytest.assert_eq(
        field.to_data(defaults = True, include_internals = True),
        expected_output,
    )
