import vampytest

from ..footer import EmbedFooter


def test__EmbedFooter__repr():
    """
    Tests whether ``EmbedFooter.__repr__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    embed_footer = EmbedFooter(text = text, icon_url = icon_url)
    vampytest.assert_instance(repr(embed_footer), str)


def test__EmbedFooter__hash():
    """
    Tests whether ``EmbedFooter.__hash__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    embed_footer = EmbedFooter(text = text, icon_url = icon_url)
    vampytest.assert_instance(hash(embed_footer), int)


def _iter_options__eq():
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    keyword_parameters = {
        'icon_url': icon_url,
        'text': text,
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
            'icon_url': 'attachment://rin.png',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'text': 'rin',
        },
        False,
    )
    

@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__EmbedFooter__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``EmbedFooter.__eq__`` works as intended.
    
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
    embed_footer_0 = EmbedFooter(**keyword_parameters_0)
    embed_footer_1 = EmbedFooter(**keyword_parameters_1)
    
    output = embed_footer_0 == embed_footer_1
    vampytest.assert_instance(output, bool)
    return output


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
    embed_footer = EmbedFooter(**keyword_parameters)
    output = bool(embed_footer)
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
    embed_footer = EmbedFooter(**keyword_parameters)
    output = len(embed_footer)
    vampytest.assert_instance(output, int)
    return output
