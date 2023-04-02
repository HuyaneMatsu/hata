import vampytest

from ..field import EmbedField


def test__EmbedField__repr():
    """
    Tests whether ``EmbedField.__repr__`` works as intended.
    """
    inline = True
    name = 'orin'
    value = 'okuu'
    
    field = EmbedField(name = name, value = value, inline = inline)
    vampytest.assert_instance(repr(field), str)


def test__EmbedField__hash():
    """
    Tests whether ``EmbedField.__hash__`` works as intended.
    """
    inline = True
    name = 'orin'
    value = 'okuu'
    
    field = EmbedField(name = name, value = value, inline = inline)
    vampytest.assert_instance(hash(field), int)


def test__EmbedField__eq():
    """
    Tests whether ``EmbedField.__eq__`` works as intended.
    """
    inline = True
    name = 'orin'
    value = 'okuu'
    
    keyword_parameters = {
        'inline': inline,
        'name': name,
        'value': value,
    }
    
    field = EmbedField(**keyword_parameters)
    
    vampytest.assert_eq(field, field)
    vampytest.assert_ne(field, object())
    
    for field_name, field_value in (
        ('inline', False),
        ('name', 'satori'),
        ('value', 'koishi'),
    ):
        test_field = EmbedField(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(field, test_field)


def test__EmbedField__bool():
    """
    Tests whether ``EmbedField.__bool__`` works as intended.
    """
    inline = True
    value = 'okuu'
    name = 'orin'
    
    for field, expected_output in (
        (EmbedField(), False),
        (EmbedField(name = name), True),
        (EmbedField(inline = inline), False),
        (EmbedField(name = name, inline = inline), True),
        (EmbedField(value = value), True),
        (EmbedField(value = value, name = name), True),
        (EmbedField(value = value, inline = inline), True),
        (EmbedField(value = value, name = name, inline = inline), True),
    ):
        vampytest.assert_eq(bool(field), expected_output)


def test__EmbedField__len():
    """
    Tests whether ``EmbedField.__len__`` works as intended.
    """
    inline = True
    value = 'okuu'
    name = 'orin'
    
    for field, expected_output in (
        (EmbedField(), 0),
        (EmbedField(name = name), len(name)),
        (EmbedField(inline = inline), 0),
        (EmbedField(name = name, inline = inline), len(name)),
        (EmbedField(value = value), len(value)),
        (EmbedField(value = value, name = name), len(name) + len(value)),
        (EmbedField(value = value, inline = inline), len(value)),
        (EmbedField(value = value, name = name, inline = inline), len(name) + len(value)),
    ):
        vampytest.assert_eq(len(field), expected_output)
