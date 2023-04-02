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


def test__EmbedThumbnail__copy_with__0():
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


def test__EmbedThumbnail__copy_with__1():
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


def test__EmbedThumbnail__contents():
    """
    Tests whether ``EmbedThumbnail.contents`` works as intended.
    """
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedThumbnail(url), set()),
    ):
        output = field.contents
        vampytest.assert_instance(output, list)
        vampytest.assert_eq({*output}, expected_output)


def test__EmbedThumbnail__iter_contents():
    """
    Tests whether ``EmbedThumbnail.iter_contents`` works as intended.
    """
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedThumbnail(url), set()),
    ):
        vampytest.assert_eq({*field.iter_contents()}, expected_output)
