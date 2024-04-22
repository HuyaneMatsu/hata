import vampytest

from ..video import EmbedVideo

from .test__EmbedVideo__constructor import _assert_fields_set


def test__EmbedVideo__clean_copy():
    """
    Tests whether ``EmbedVideo.clean_copy`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedVideo(url)
    copy = field.clean_copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(copy.url, url)


def test__EmbedVideo__copy():
    """
    Tests whether ``EmbedVideo.copy`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedVideo(url)
    copy = field.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedVideo__copy_with__no_fields():
    """
    Tests whether ``EmbedVideo.copy_with`` works as intended.
    
    Case: No fields given.
    """
    url = 'https://orindance.party/'
    
    field = EmbedVideo(url)
    copy = field.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedVideo__copy_with__all_fields():
    """
    Tests whether ``EmbedVideo.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_url = 'https://orindance.party/'
    
    new_url = 'https://www.astil.dev/'
    
    field = EmbedVideo(old_url)
    copy = field.copy_with(
        url = new_url,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(copy.url, new_url)


def _iter_options__contents():
    url = 'https://orindance.party/'
    
    yield {}, set()
    yield {'url': url}, set()


@vampytest._(vampytest.call_from(_iter_options__contents()).returning_last())
def test__EmbedVideo__contents(keyword_parameters):
    """
    Tests whether ``EmbedVideo.contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed video with.
    
    Returns
    -------
    output : `set<str>`
    """
    field = EmbedVideo(**keyword_parameters)
    output = field.contents
    vampytest.assert_instance(output, list)
    return {*output}


def _iter_options__iter_contents():
    url = 'https://orindance.party/'
    
    yield {}, set()
    yield {'url': url}, set()


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__EmbedVideo__iter_contents(keyword_parameters):
    """
    Tests whether ``EmbedVideo.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed video with.
    
    Returns
    -------
    output : `set<str>`
    """
    field = EmbedVideo(**keyword_parameters)
    return {*field.iter_contents()}
