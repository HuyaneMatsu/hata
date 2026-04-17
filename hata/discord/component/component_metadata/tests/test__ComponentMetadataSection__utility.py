import vampytest

from ....guild import Guild
from ....user import GuildProfile, User

from ...component import Component, ComponentType
from ...media_info import MediaInfo

from ..section import ComponentMetadataSection

from .test__ComponentMetadataSection__constructor import _assert_fields_set


def test__ComponentMetadataSection__clean_copy():
    """
    Tests whether ``ComponentMetadataSection.clean_copy`` works as intended.
    """
    guild_id = 202505030026
    guild = Guild.precreate(guild_id)
    
    user = User.precreate(202505030027, name = 'Koishi')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'koi')
    
    components = [
        Component(ComponentType.text_display, content = f'{user.mention}'),
    ]
    thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component_metadata = ComponentMetadataSection(
        components = components,
        thumbnail = thumbnail,
    )
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_ne(copy, component_metadata)
    
    vampytest.assert_eq(
        copy.components,
        (
            Component(ComponentType.text_display, content = f'@{user.name_at(guild)}'),
        ),
    )
    vampytest.assert_eq(copy.thumbnail, thumbnail)


def test__ComponentMetadataSection__copy():
    """
    Tests whether ``ComponentMetadataSection.copy`` works as intended.
    """
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component_metadata = ComponentMetadataSection(
        components = components,
        thumbnail = thumbnail,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataSection__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataSection.copy_with`` works as intended.
    
    Case: no fields.
    """
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component_metadata = ComponentMetadataSection(
        components = components,
        thumbnail = thumbnail,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataSection__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataSection.copy_with`` works as intended.
    
    Case: all fields.
    """
    old_components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    old_thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    new_components = [
        Component(ComponentType.text_display, content = 'yuina'),
    ]
    new_thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://big_braids_orin.png'),
    )
    
    component_metadata = ComponentMetadataSection(
        components = old_components,
        thumbnail = old_thumbnail,
    )
    copy = component_metadata.copy_with(
        components = new_components,
        thumbnail = new_thumbnail,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    
    vampytest.assert_eq(copy.components, tuple(new_components))
    vampytest.assert_eq(copy.thumbnail, new_thumbnail)


def test__ComponentMetadataSection__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataSection.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields.
    """
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component_metadata = ComponentMetadataSection(
        components = components,
        thumbnail = thumbnail,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataSection__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataSection.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields.
    """
    old_components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    old_thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    new_components = [
        Component(ComponentType.text_display, content = 'yuina'),
    ]
    new_thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://big_braids_orin.png'),
    )
    
    component_metadata = ComponentMetadataSection(
        components = old_components,
        thumbnail = old_thumbnail,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'components': new_components,
        'thumbnail': new_thumbnail,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    
    vampytest.assert_eq(copy.components, tuple(new_components))
    vampytest.assert_eq(copy.thumbnail, new_thumbnail)


def _iter_options__iter_contents():
    content_0 = 'chata'
    content_1 = 'important'
    
    components = [
        Component(ComponentType.text_display, content = content_0),
        Component(ComponentType.text_display, content = content_1),
    ]
    thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://big_braids_orin.png'),
    )
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'components': components,
            'thumbnail': thumbnail,
        },
        [
            content_0,
            content_1,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataSection__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataSection.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataSection(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
