import vampytest

from ....user import User

from ..field import EmbedField

from .test__EmbedField__constructor import _assert_fields_set


def test__EmbedField__clean_copy():
    """
    Tests whether ``EmbedField.clean_copy`` works as intended.
    """
    user_0 = User.precreate(202303310001, name = 'koishi')
    user_1 = User.precreate(202303310002, name = 'satori')
    
    inline = True
    name = user_0.mention
    value = user_1.mention
    
    field = EmbedField(name = name, value = value, inline = inline)
    copy = field.clean_copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(copy.inline, inline)
    vampytest.assert_eq(copy.name, f'@{user_0.name}')
    vampytest.assert_eq(copy.value, f'@{user_1.name}')


def test__EmbedField__copy():
    """
    Tests whether ``EmbedField.copy`` works as intended.
    """
    inline = True
    name = 'orin'
    value = 'okuu'
    
    field = EmbedField(name = name, value = value, inline = inline)
    copy = field.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedField__copy_with__0():
    """
    Tests whether ``EmbedField.copy_with`` works as intended.
    
    Case: No fields given.
    """
    inline = True
    name = 'orin'
    value = 'okuu'
    
    field = EmbedField(name = name, value = value, inline = inline)
    copy = field.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedField__copy_with__1():
    """
    Tests whether ``EmbedField.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_inline = True
    old_name = 'orin'
    old_value = 'okuu'
    
    new_inline = False
    new_name = 'koishi'
    new_value = 'satori'
    
    field = EmbedField(name = old_name, value = old_value, inline = old_inline)
    copy = field.copy_with(
        inline = new_inline,
        name = new_name,
        value = new_value,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(copy.inline, new_inline)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.value, new_value)


def test__EmbedField__contents():
    """
    Tests whether ``EmbedField.contents`` works as intended.
    """
    inline = True
    name = 'orin'
    value = 'okuu'
    
    for field, expected_output in (
        (EmbedField(), set()),
        (EmbedField(name = name), {name}),
        (EmbedField(inline = inline), set()),
        (EmbedField(value = value), {value}),
        (EmbedField(name = name, inline = inline), {name}),
        (EmbedField(name = name, value = value,), {name, value}),
        (EmbedField(value = value, inline = inline), {value}),
        (EmbedField(name = name, value = value, inline = inline), {name, value}),
    ):
        output = field.contents
        vampytest.assert_instance(output, list)
        vampytest.assert_eq({*output}, expected_output)


def test__EmbedField__iter_contents():
    """
    Tests whether ``EmbedField.iter_contents`` works as intended.
    """
    inline = True
    name = 'orin'
    value = 'okuu'
    
    for field, expected_output in (
        (EmbedField(), set()),
        (EmbedField(name = name), {name}),
        (EmbedField(inline = inline), set()),
        (EmbedField(value = value), {value}),
        (EmbedField(name = name, inline = inline), {name}),
        (EmbedField(name = name, value = value,), {name, value}),
        (EmbedField(value = value, inline = inline), {value}),
        (EmbedField(name = name, value = value, inline = inline), {name, value}),
    ):
        vampytest.assert_eq({*field.iter_contents()}, expected_output)
