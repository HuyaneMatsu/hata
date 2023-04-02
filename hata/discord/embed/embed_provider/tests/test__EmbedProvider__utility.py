import vampytest

from ....user import User

from ..provider import EmbedProvider

from .test__EmbedProvider__constructor import _assert_fields_set


def test__EmbedProvider__clean_copy():
    """
    Tests whether ``EmbedProvider.clean_copy`` works as intended.
    """
    user = User.precreate(202303310004, name = 'koishi')
    
    name = user.mention
    url = 'https://orindance.party/'
    
    field = EmbedProvider(name = name, url = url)
    copy = field.clean_copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(copy.name, f'@{user.name}')
    vampytest.assert_eq(copy.url, url)


def test__EmbedProvider__copy():
    """
    Tests whether ``EmbedProvider.copy`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    field = EmbedProvider(name = name, url = url)
    copy = field.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedProvider__copy_with__0():
    """
    Tests whether ``EmbedProvider.copy_with`` works as intended.
    
    Case: No fields given.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    field = EmbedProvider(name = name, url = url)
    copy = field.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedProvider__copy_with__1():
    """
    Tests whether ``EmbedProvider.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_name = 'orin'
    old_url = 'https://orindance.party/'
    
    new_name = 'rin'
    new_url = 'https://www.astil.dev/'
    
    field = EmbedProvider(name = old_name, url = old_url)
    copy = field.copy_with(
        name = new_name,
        url = new_url,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.url, new_url)


def test__EmbedProvider__contents():
    """
    Tests whether ``EmbedProvider.contents`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedProvider(), set()),
        (EmbedProvider(name = name), {name}),
        (EmbedProvider(url = url), set()),
        (EmbedProvider(name = name, url = url), {name}),
    ):
        output = field.contents
        vampytest.assert_instance(output, list)
        vampytest.assert_eq({*output}, expected_output)


def test__EmbedProvider__iter_contents():
    """
    Tests whether ``EmbedProvider.iter_contents`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedProvider(), set()),
        (EmbedProvider(name = name), {name}),
        (EmbedProvider(url = url), set()),
        (EmbedProvider(name = name, url = url), {name}),
    ):
        vampytest.assert_eq({*field.iter_contents()}, expected_output)
