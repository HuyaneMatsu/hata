import vampytest

from ..field import EmbedField


def _assert_fields_set(embed_field):
    """
    Checks whether every fields of the given embed field are set.
    
    Parameters
    ----------
    embed_field : ``EmbedField``
        The field to check.
    """
    vampytest.assert_instance(embed_field, EmbedField)
    vampytest.assert_instance(embed_field.inline, bool)
    vampytest.assert_instance(embed_field.name, str, nullable = True)
    vampytest.assert_instance(embed_field.value, str, nullable = True)


def test__EmbedField__new__no_fields():
    """
    Tests whether ``EmbedField.__new__`` works as intended.
    
    Case: Minimal amount of parameters.
    """
    embed_field = EmbedField()
    _assert_fields_set(embed_field)


def test__EmbedField__new__all_fields():
    """
    Tests whether ``EmbedField.__new__`` works as intended.
    
    Case: Maximal amount of parameters.
    """
    inline = True
    name = 'orin'
    value = 'okuu'
    
    embed_field = EmbedField(name = name, value = value, inline = inline)
    _assert_fields_set(embed_field)
    
    vampytest.assert_eq(embed_field.inline, inline)
    vampytest.assert_eq(embed_field.name, name)
    vampytest.assert_eq(embed_field.value, value)


def test__EmbedField__new__string_conversion():
    """
    Tests whether ``EmbedField.__new__`` works as intended.
    
    Case: name & value conversion check.
    """
    name = 123
    value = 456
    
    embed_field = EmbedField(name = name, value = value)
    _assert_fields_set(embed_field)
    
    vampytest.assert_eq(embed_field.name, str(name))
    vampytest.assert_eq(embed_field.value, str(value))
