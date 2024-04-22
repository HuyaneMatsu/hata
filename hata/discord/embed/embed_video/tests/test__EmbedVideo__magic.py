import vampytest

from ..video import EmbedVideo


def test__EmbedVideo__repr():
    """
    Tests whether ``EmbedVideo.__repr__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedVideo(url)
    vampytest.assert_instance(repr(field), str)


def test__EmbedVideo__hash():
    """
    Tests whether ``EmbedVideo.__hash__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedVideo(url)
    vampytest.assert_instance(hash(field), int)


def test__EmbedVideo__eq():
    """
    Tests whether ``EmbedVideo.__eq__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    keyword_parameters = {
        'url': url,
    }
    
    field = EmbedVideo(**keyword_parameters)
    
    vampytest.assert_eq(field, field)
    vampytest.assert_ne(field, object())
    
    for field_name, field_value in (
        ('url', 'https://www.astil.dev/'),
    ):
        test_field = EmbedVideo(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(field, test_field)


def _iter_options__bool():
    url = 'https://orindance.party/'
    
    yield {}, False
    yield {'url': url}, True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__EmbedVideo__bool(keyword_parameters):
    """
    Tests whether ``EmbedVideo.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed video with.
    
    Returns
    -------
    output : `bool`
    """
    field = EmbedVideo(**keyword_parameters)
    output = bool(field)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    url = 'https://orindance.party/'
    
    yield {}, 0
    yield {'url': url}, 0


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__EmbedVideo__len(keyword_parameters):
    """
    Tests whether ``EmbedVideo.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed video with.
    
    Returns
    -------
    output : `int`
    """
    field = EmbedVideo(**keyword_parameters)
    output = len(field)
    vampytest.assert_instance(output, int)
    return output
