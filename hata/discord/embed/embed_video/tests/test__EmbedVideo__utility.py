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


def test__EmbedVideo__copy_with__0():
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


def test__EmbedVideo__copy_with__1():
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


def test__EmbedVideo__contents():
    """
    Tests whether ``EmbedVideo.contents`` works as intended.
    """
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedVideo(url), set()),
    ):
        output = field.contents
        vampytest.assert_instance(output, list)
        vampytest.assert_eq({*output}, expected_output)


def test__EmbedVideo__iter_contents():
    """
    Tests whether ``EmbedVideo.iter_contents`` works as intended.
    """
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedVideo(url), set()),
    ):
        vampytest.assert_eq({*field.iter_contents()}, expected_output)
