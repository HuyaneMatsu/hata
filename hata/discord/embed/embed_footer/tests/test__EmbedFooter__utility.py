import vampytest

from ....user import User

from ..footer import EmbedFooter

from .test__EmbedFooter__constructor import _assert_fields_set


def test__EmbedFooter__clean_copy():
    """
    Tests whether ``EmbedFooter.clean_copy`` works as intended.
    """
    user = User.precreate(202303310003, name = 'koishi')
    
    icon_url = 'attachment://orin.png'
    text = user.mention
    
    field = EmbedFooter(text = text, icon_url = icon_url)
    copy = field.clean_copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(copy.icon_url, icon_url)
    vampytest.assert_eq(copy.text, f'@{user.name}')


def test__EmbedFooter__copy():
    """
    Tests whether ``EmbedFooter.copy`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    field = EmbedFooter(text = text, icon_url = icon_url)
    copy = field.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedFooter__copy_with__0():
    """
    Tests whether ``EmbedFooter.copy_with`` works as intended.
    
    Case: No fields given.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    field = EmbedFooter(text = text, icon_url = icon_url)
    copy = field.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedFooter__copy_with__1():
    """
    Tests whether ``EmbedFooter.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_icon_url = 'attachment://orin.png'
    old_text = 'orin'
    
    new_icon_url = 'attachment://rin.png'
    new_text = 'rin'
    
    field = EmbedFooter(text = old_text, icon_url = old_icon_url)
    copy = field.copy_with(
        icon_url = new_icon_url,
        text = new_text,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(copy.icon_url, new_icon_url)
    vampytest.assert_eq(copy.text, new_text)


def test__EmbedFooter__contents():
    """
    Tests whether ``EmbedFooter.contents`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedFooter(), set()),
        (EmbedFooter(text = text), {text}),
        (EmbedFooter(icon_url = icon_url), set()),
        (EmbedFooter(text = text, icon_url = icon_url), {text}),
    ):
        output = field.contents
        vampytest.assert_instance(output, list)
        vampytest.assert_eq({*output}, expected_output)


def test__EmbedFooter__iter_contents():
    """
    Tests whether ``EmbedFooter.iter_contents`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    for field, expected_output in (
        (EmbedFooter(), set()),
        (EmbedFooter(text = text), {text}),
        (EmbedFooter(icon_url = icon_url), set()),
        (EmbedFooter(text = text, icon_url = icon_url), {text}),
    ):
        vampytest.assert_eq({*field.iter_contents()}, expected_output)
