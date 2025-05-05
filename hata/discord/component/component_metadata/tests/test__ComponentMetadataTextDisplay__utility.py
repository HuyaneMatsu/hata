import vampytest

from ....guild import Guild
from ....user import GuildProfile, User

from ..text_display import ComponentMetadataTextDisplay

from .test__ComponentMetadataTextDisplay__constructor import _assert_fields_set


def test__ComponentMetadataTextDisplay__clean_copy():
    """
    Tests whether ``ComponentMetadataTextDisplay.clean_copy`` works as intended.
    """
    guild_id = 202505030030
    guild = Guild.precreate(guild_id)
    
    user = User.precreate(202505030031, name = 'koishi')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'koi')
    
    content = f'{user.mention}'
    
    component_metadata = ComponentMetadataTextDisplay(
        content = content,
    )
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_ne(copy, component_metadata)
    
    vampytest.assert_eq(copy.content, f'@{user.name_at(guild)}')


def test__ComponentMetadataTextDisplay__copy():
    """
    Tests whether ``ComponentMetadataTextDisplay.copy`` works as intended.
    """
    content = 'hey sister'
    
    component_metadata = ComponentMetadataTextDisplay(
        content = content,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataTextDisplay__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataTextDisplay.copy_with`` works as intended.
    
    Case: no fields.
    """
    content = 'hey sister'
    
    component_metadata = ComponentMetadataTextDisplay(
        content = content,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataTextDisplay__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataTextDisplay.copy_with`` works as intended.
    
    Case: all fields.
    """
    old_content = 'hey sister'
    
    new_content = 'hey mister'
    
    component_metadata = ComponentMetadataTextDisplay(
        content = old_content,
    )
    copy = component_metadata.copy_with(
        content = new_content,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.content, new_content)


def test__ComponentMetadataTextDisplay__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataTextDisplay.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields.
    """
    content = 'hey sister'
    
    component_metadata = ComponentMetadataTextDisplay(
        content = content,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataTextDisplay__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataTextDisplay.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields.
    """
    old_content = 'hey sister'
    
    new_content = 'hey mister'
    
    component_metadata = ComponentMetadataTextDisplay(
        content = old_content,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'content': new_content,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.content, new_content)


def _iter_options__iter_contents():
    content = 'lie'
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'content': content,
        },
        [
            content,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataTextDisplay__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataTextDisplay.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataTextDisplay(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
