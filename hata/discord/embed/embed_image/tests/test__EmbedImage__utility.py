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


def test__EmbedImage__copy_with__0():
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


def test__EmbedImage__copy_with__1():
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


def test__EmbedImage__contents():
    """
    Tests whether ``EmbedImage.contents`` works as intended.
    """
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedImage(url), set()),
    ):
        output = field.contents
        vampytest.assert_instance(output, list)
        vampytest.assert_eq({*output}, expected_output)


def test__EmbedImage__iter_contents():
    """
    Tests whether ``EmbedImage.iter_contents`` works as intended.
    """
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedImage(url), set()),
    ):
        vampytest.assert_eq({*field.iter_contents()}, expected_output)
