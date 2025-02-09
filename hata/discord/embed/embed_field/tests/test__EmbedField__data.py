import vampytest

from ..field import EmbedField

from .test__EmbedField__constructor import _assert_fields_set


def test__EmbedField__from_data():
    """
    Tests whether ``EmbedField.from_data`` works as intended.
    """
    inline = True
    name = 'orin'
    value = 'okuu'
    
    data = {
        'inline': inline,
        'name': name,
        'value': value,
    }
    
    embed_field = EmbedField.from_data(data)
    _assert_fields_set(embed_field)
    
    vampytest.assert_eq(embed_field.inline, inline)
    vampytest.assert_eq(embed_field.name, name)
    vampytest.assert_eq(embed_field.value, value)


def test__EmbedField__to_data():
    """
    Tests whether ``EmbedField.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    inline = True
    name = 'orin'
    value = 'okuu'
    
    embed_field = EmbedField(name = name, value = value, inline = inline)
    
    expected_output = {
        'inline': inline,
        'name': name,
        'value': value,
    }
    
    vampytest.assert_eq(
        embed_field.to_data(defaults = True, include_internals = True),
        expected_output,
    )
