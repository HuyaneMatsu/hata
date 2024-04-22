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


def _iter_options__bool():
    inline = True
    value = 'okuu'
    name = 'yuuka'
    
    yield {}, False
    yield {'name': name}, True
    yield {'value': value}, True
    yield {'name': name, 'value': value}, True
    yield {'inline': inline}, False
    yield {'inline': inline, 'name': name}, True
    yield {'inline': inline, 'value': value}, True
    yield {'inline': inline, 'name': name, 'value': value}, True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__EmbedField__bool(keyword_parameters):
    """
    Tests whether ``EmbedField.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed field with.
    
    Returns
    -------
    output : `bool`
    """
    field = EmbedField(**keyword_parameters)
    output = bool(field)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    inline = True
    value = 'okuu'
    name = 'yuuka'
    
    yield {}, 0
    yield {'name': name}, len(name)
    yield {'value': value}, len(value)
    yield {'name': name, 'value': value}, len(name) + len(value)
    yield {'inline': inline}, 0
    yield {'inline': inline, 'name': name}, len(name)
    yield {'inline': inline, 'value': value}, len(value)
    yield {'inline': inline, 'name': name, 'value': value}, len(name) + len(value)


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__EmbedField__len(keyword_parameters):
    """
    Tests whether ``EmbedField.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed field with.
    
    Returns
    -------
    output : `int`
    """
    field = EmbedField(**keyword_parameters)
    output = len(field)
    vampytest.assert_instance(output, int)
    return output
