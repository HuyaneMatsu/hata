import vampytest

from ..thumbnail import EmbedThumbnail

from .test__EmbedThumbnail__constructor import _assert_fields_set


def test__EmbedThumbnail__clean_copy():
    """
    Tests whether ``EmbedThumbnail.clean_copy`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedThumbnail(url)
    copy = field.clean_copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(copy.url, url)


def test__EmbedThumbnail__copy():
    """
    Tests whether ``EmbedThumbnail.copy`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedThumbnail(url)
    copy = field.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedThumbnail__copy_with__no_fields():
    """
    Tests whether ``EmbedThumbnail.copy_with`` works as intended.
    
    Case: No fields given.
    """
    url = 'https://orindance.party/'
    
    field = EmbedThumbnail(url)
    copy = field.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedThumbnail__copy_with__all_fields():
    """
    Tests whether ``EmbedThumbnail.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_url = 'https://orindance.party/'
    
    new_url = 'https://www.astil.dev/'
    
    field = EmbedThumbnail(old_url)
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
def test__EmbedThumbnail__contents(keyword_parameters):
    """
    Tests whether ``EmbedThumbnail.contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed thumbnail with.
    
    Returns
    -------
    output : `set<str>`
    """
    field = EmbedThumbnail(**keyword_parameters)
    output = field.contents
    vampytest.assert_instance(output, list)
    return {*output}


def _iter_options__iter_contents():
    url = 'https://orindance.party/'
    
    yield {}, set()
    yield {'url': url}, set()


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__EmbedThumbnail__iter_contents(keyword_parameters):
    """
    Tests whether ``EmbedThumbnail.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed thumbnail with.
    
    Returns
    -------
    output : `set<str>`
    """
    field = EmbedThumbnail(**keyword_parameters)
    return {*field.iter_contents()}
