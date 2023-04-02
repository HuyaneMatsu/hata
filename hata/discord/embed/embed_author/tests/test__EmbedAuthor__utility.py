import vampytest

from ....user import User

from ..author import EmbedAuthor

from .test__EmbedAuthor__constructor import _assert_fields_set


def test__EmbedAuthor__clean_copy():
    """
    Tests whether ``EmbedAuthor.clean_copy`` works as intended.
    """
    user = User.precreate(202303310000, name = 'koishi')
    
    icon_url = 'attachment://orin.png'
    name = user.mention
    url = 'https://orindance.party/'
    
    field = EmbedAuthor(name = name, icon_url = icon_url, url = url)
    copy = field.clean_copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(copy.icon_url, icon_url)
    vampytest.assert_eq(copy.name, f'@{user.name}')
    vampytest.assert_eq(copy.url, url)


def test__EmbedAuthor__copy():
    """
    Tests whether ``EmbedAuthor.copy`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    field = EmbedAuthor(name = name, icon_url = icon_url, url = url)
    copy = field.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedAuthor__copy_with__0():
    """
    Tests whether ``EmbedAuthor.copy_with`` works as intended.
    
    Case: No fields given.
    """
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    field = EmbedAuthor(name = name, icon_url = icon_url, url = url)
    copy = field.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedAuthor__copy_with__1():
    """
    Tests whether ``EmbedAuthor.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_icon_url = 'attachment://orin.png'
    old_name = 'orin'
    old_url = 'https://orindance.party/'
    
    new_icon_url = 'attachment://rin.png'
    new_name = 'rin'
    new_url = 'https://www.astil.dev/'
    
    field = EmbedAuthor(name = old_name, icon_url = old_icon_url, url = old_url)
    copy = field.copy_with(
        icon_url = new_icon_url,
        name = new_name,
        url = new_url,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(copy.icon_url, new_icon_url)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.url, new_url)


def test__EmbedAuthor__contents():
    """
    Tests whether ``EmbedAuthor.contents`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedAuthor(), set()),
        (EmbedAuthor(name = name), {name}),
        (EmbedAuthor(url = url), set()),
        (EmbedAuthor(name = name, url = url), {name}),
        (EmbedAuthor(name = name, icon_url = icon_url,), {name}),
        (EmbedAuthor(icon_url = icon_url, url = url), set()),
        (EmbedAuthor(name = name, icon_url = icon_url, url = url), {name}),
    ):
        output = field.contents
        vampytest.assert_instance(output, list)
        vampytest.assert_eq({*output}, expected_output)


def test__EmbedAuthor__iter_contents():
    """
    Tests whether ``EmbedAuthor.iter_contents`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedAuthor(), set()),
        (EmbedAuthor(name = name), {name}),
        (EmbedAuthor(url = url), set()),
        (EmbedAuthor(name = name, url = url), {name}),
        (EmbedAuthor(name = name, icon_url = icon_url,), {name}),
        (EmbedAuthor(icon_url = icon_url, url = url), set()),
        (EmbedAuthor(name = name, icon_url = icon_url, url = url), {name}),
    ):
        vampytest.assert_eq({*field.iter_contents()}, expected_output)
