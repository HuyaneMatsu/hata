import vampytest

from ..footer import EmbedFooter


def test__EmbedFooter__repr():
    """
    Tests whether ``EmbedFooter.__repr__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    field = EmbedFooter(text = text, icon_url = icon_url)
    vampytest.assert_instance(repr(field), str)


def test__EmbedFooter__hash():
    """
    Tests whether ``EmbedFooter.__hash__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    field = EmbedFooter(text = text, icon_url = icon_url)
    vampytest.assert_instance(hash(field), int)


def test__EmbedFooter__eq():
    """
    Tests whether ``EmbedFooter.__eq__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    keyword_parameters = {
        'icon_url': icon_url,
        'text': text,
    }
    
    field = EmbedFooter(**keyword_parameters)
    
    vampytest.assert_eq(field, field)
    vampytest.assert_ne(field, object())
    
    for field_name, field_value in (
        ('icon_url', 'attachment://rin.png'),
        ('text', 'rin'),
    ):
        test_field = EmbedFooter(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(field, test_field)


def _iter_options__bool():
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    yield {}, False
    yield {'text': text}, True
    yield {'icon_url': icon_url}, True
    yield {'text': text, 'icon_url': icon_url}, True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__EmbedFooter__bool(keyword_parameters):
    """
    Tests whether ``EmbedFooter.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed footer with.
    
    Returns
    -------
    output : `bool`
    """
    field = EmbedFooter(**keyword_parameters)
    output = bool(field)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    yield {}, 0
    yield {'text': text}, len(text)
    yield {'icon_url': icon_url}, 0
    yield {'text': text, 'icon_url': icon_url}, len(text)


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__EmbedFooter__len(keyword_parameters):
    """
    Tests whether ``EmbedFooter.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed footer with.
    
    Returns
    -------
    output : `int`
    """
    field = EmbedFooter(**keyword_parameters)
    output = len(field)
    vampytest.assert_instance(output, int)
    return output
