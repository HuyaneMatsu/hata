import vampytest

from ..field import EmbedField


def test__EmbedField__repr():
    """
    Tests whether ``EmbedField.__repr__`` works as intended.
    """
    inline = True
    name = 'orin'
    value = 'okuu'
    
    embed_field = EmbedField(name = name, value = value, inline = inline)
    vampytest.assert_instance(repr(embed_field), str)


def test__EmbedField__hash():
    """
    Tests whether ``EmbedField.__hash__`` works as intended.
    """
    inline = True
    name = 'orin'
    value = 'okuu'
    
    embed_field = EmbedField(name = name, value = value, inline = inline)
    vampytest.assert_instance(hash(embed_field), int)


def _iter_options__eq():
    inline = True
    name = 'orin'
    value = 'okuu'
    
    keyword_parameters = {
        'inline': inline,
        'name': name,
        'value': value,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'inline': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'satori',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'value': 'koishi',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__EmbedField__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``EmbedField.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    embed_field_0 = EmbedField(**keyword_parameters_0)
    embed_field_1 = EmbedField(**keyword_parameters_1)
    
    output = embed_field_0 == embed_field_1
    vampytest.assert_instance(output, bool)
    return output


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
    embed_field = EmbedField(**keyword_parameters)
    output = bool(embed_field)
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
    embed_field = EmbedField(**keyword_parameters)
    output = len(embed_field)
    vampytest.assert_instance(output, int)
    return output
