import vampytest

from ..thumbnail import EmbedThumbnail


def test__EmbedThumbnail__repr():
    """
    Tests whether ``EmbedThumbnail.__repr__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedThumbnail(url)
    vampytest.assert_instance(repr(field), str)


def test__EmbedThumbnail__hash():
    """
    Tests whether ``EmbedThumbnail.__hash__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedThumbnail(url)
    vampytest.assert_instance(hash(field), int)


def test__EmbedThumbnail__eq():
    """
    Tests whether ``EmbedThumbnail.__eq__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    keyword_parameters = {
        'url': url,
    }
    
    field = EmbedThumbnail(**keyword_parameters)
    
    vampytest.assert_eq(field, field)
    vampytest.assert_ne(field, object())
    
    for field_name, field_value in (
        ('url', 'https://www.astil.dev/'),
    ):
        test_field = EmbedThumbnail(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(field, test_field)


def _iter_options__bool():
    url = 'https://orindance.party/'
    
    yield {}, False
    yield {'url': url}, True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__EmbedThumbnail__bool(keyword_parameters):
    """
    Tests whether ``EmbedThumbnail.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed thumbnail with.
    
    Returns
    -------
    output : `bool`
    """
    field = EmbedThumbnail(**keyword_parameters)
    output = bool(field)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    url = 'https://orindance.party/'
    
    yield {}, 0
    yield {'url': url}, 0


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__EmbedThumbnail__len(keyword_parameters):
    """
    Tests whether ``EmbedThumbnail.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed thumbnail with.
    
    Returns
    -------
    output : `int`
    """
    field = EmbedThumbnail(**keyword_parameters)
    output = len(field)
    vampytest.assert_instance(output, int)
    return output
