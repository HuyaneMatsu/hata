import vampytest

from ..thumbnail import EmbedThumbnail

from .test__EmbedThumbnail__constructor import _assert_fields_set


def test__EmbedThumbnail__clean_copy():
    """
    Tests whether ``EmbedThumbnail.clean_copy`` works as intended.
    """
    url = 'https://orindance.party/'
    
    embed_thumbnail = EmbedThumbnail(url)
    copy = embed_thumbnail.clean_copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed_thumbnail, copy)
    
    vampytest.assert_eq(copy.url, url)


def test__EmbedThumbnail__copy():
    """
    Tests whether ``EmbedThumbnail.copy`` works as intended.
    """
    url = 'https://orindance.party/'
    
    embed_thumbnail = EmbedThumbnail(url)
    copy = embed_thumbnail.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed_thumbnail, copy)
    
    vampytest.assert_eq(embed_thumbnail, copy)


def test__EmbedThumbnail__copy_with__no_fields():
    """
    Tests whether ``EmbedThumbnail.copy_with`` works as intended.
    
    Case: No fields given.
    """
    url = 'https://orindance.party/'
    
    embed_thumbnail = EmbedThumbnail(url)
    copy = embed_thumbnail.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed_thumbnail, copy)
    
    vampytest.assert_eq(embed_thumbnail, copy)


def test__EmbedThumbnail__copy_with__all_fields():
    """
    Tests whether ``EmbedThumbnail.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_url = 'https://orindance.party/'
    
    new_url = 'https://www.astil.dev/'
    
    embed_thumbnail = EmbedThumbnail(old_url)
    copy = embed_thumbnail.copy_with(
        url = new_url,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed_thumbnail, copy)
    
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
    embed_thumbnail = EmbedThumbnail(**keyword_parameters)
    output = embed_thumbnail.contents
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
    embed_thumbnail = EmbedThumbnail(**keyword_parameters)
    return {*embed_thumbnail.iter_contents()}
