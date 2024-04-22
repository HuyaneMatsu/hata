import vampytest

from ..image import EmbedImage

from .test__EmbedImage__constructor import _assert_fields_set


def test__EmbedImage__clean_copy():
    """
    Tests whether ``EmbedImage.clean_copy`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedImage(url)
    copy = field.clean_copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(copy.url, url)


def test__EmbedImage__copy():
    """
    Tests whether ``EmbedImage.copy`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedImage(url)
    copy = field.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedImage__copy_with__no_fields():
    """
    Tests whether ``EmbedImage.copy_with`` works as intended.
    
    Case: No fields given.
    """
    url = 'https://orindance.party/'
    
    field = EmbedImage(url)
    copy = field.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedImage__copy_with__all_fields():
    """
    Tests whether ``EmbedImage.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_url = 'https://orindance.party/'
    
    new_url = 'https://www.astil.dev/'
    
    field = EmbedImage(old_url)
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
def test__EmbedImage__contents(keyword_parameters):
    """
    Tests whether ``EmbedImage.contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed image with.
    
    Returns
    -------
    output : `set<str>`
    """
    field = EmbedImage(**keyword_parameters)
    output = field.contents
    vampytest.assert_instance(output, list)
    return {*output}


def _iter_options__iter_contents():
    url = 'https://orindance.party/'
    
    yield {}, set()
    yield {'url': url}, set()


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__EmbedImage__iter_contents(keyword_parameters):
    """
    Tests whether ``EmbedImage.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed image with.
    
    Returns
    -------
    output : `set<str>`
    """
    field = EmbedImage(**keyword_parameters)
    return {*field.iter_contents()}
