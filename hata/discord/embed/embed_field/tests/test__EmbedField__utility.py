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
    
    embed_field = EmbedField(name = name, value = value, inline = inline)
    copy = embed_field.clean_copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed_field, copy)
    
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
    
    embed_field = EmbedField(name = name, value = value, inline = inline)
    copy = embed_field.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed_field, copy)
    
    vampytest.assert_eq(embed_field, copy)


def test__EmbedField__copy_with__no_fields():
    """
    Tests whether ``EmbedField.copy_with`` works as intended.
    
    Case: No fields given.
    """
    inline = True
    name = 'orin'
    value = 'okuu'
    
    embed_field = EmbedField(name = name, value = value, inline = inline)
    copy = embed_field.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed_field, copy)
    
    vampytest.assert_eq(embed_field, copy)


def test__EmbedField__copy_with__all_fields():
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
    
    embed_field = EmbedField(name = old_name, value = old_value, inline = old_inline)
    copy = embed_field.copy_with(
        inline = new_inline,
        name = new_name,
        value = new_value,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed_field, copy)
    
    vampytest.assert_eq(copy.inline, new_inline)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.value, new_value)


def _iter_options__contents():
    inline = True
    value = 'okuu'
    name = 'yuuka'
    
    yield {}, set()
    yield {'name': name}, {name}
    yield {'value': value}, {value}
    yield {'name': name, 'value': value}, {name, value}
    yield {'inline': inline}, set()
    yield {'inline': inline, 'name': name}, {name}
    yield {'inline': inline, 'value': value}, {value}
    yield {'inline': inline, 'name': name, 'value': value}, {name, value}


@vampytest._(vampytest.call_from(_iter_options__contents()).returning_last())
def test__EmbedField__contents(keyword_parameters):
    """
    Tests whether ``EmbedField.contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed field with.
    
    Returns
    -------
    output : `set<str>`
    """
    embed_field = EmbedField(**keyword_parameters)
    output = embed_field.contents
    vampytest.assert_instance(output, list)
    return {*output}


def _iter_options__iter_contents():
    inline = True
    value = 'okuu'
    name = 'yuuka'
    
    yield {}, set()
    yield {'name': name}, {name}
    yield {'value': value}, {value}
    yield {'name': name, 'value': value}, {name, value}
    yield {'inline': inline}, set()
    yield {'inline': inline, 'name': name}, {name}
    yield {'inline': inline, 'value': value}, {value}
    yield {'inline': inline, 'name': name, 'value': value}, {name, value}


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__EmbedField__iter_contents(keyword_parameters):
    """
    Tests whether ``EmbedField.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed field with.
    
    Returns
    -------
    output : `set<str>`
    """
    embed_field = EmbedField(**keyword_parameters)
    return {*embed_field.iter_contents()}
