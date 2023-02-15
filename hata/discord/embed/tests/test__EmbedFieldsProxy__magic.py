import vampytest

from ..embed import _EmbedFieldsProxy


def test__EmbedFieldsProxy__repr():
    """
    Tests whether ``_EmbedFieldsProxy.__repr__`` works as intended.
    """
    fields = _EmbedFieldsProxy([])
    fields.add_field(*'ab')
    fields.add_field(*'cd')
    
    vampytest.assert_instance(repr(fields), str)
