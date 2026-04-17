import vampytest

from ....color import Color
from ....guild import Guild
from ....user import GuildProfile, User

from ...component import Component, ComponentType

from ..container import ComponentMetadataContainer

from .test__ComponentMetadataContainer__constructor import _assert_fields_set


def test__ComponentMetadataContainer__clean_copy():
    """
    Tests whether ``ComponentMetadataContainer.clean_copy`` works as intended.
    """
    guild_id = 202505030016
    guild = Guild.precreate(guild_id)
    
    user = User.precreate(202505030017, name = 'Koishi')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'koi')
    
    color = Color.from_rgb(12, 255, 26)
    components = [
        Component(ComponentType.text_display, content = f'{user.mention}'),
    ]
    spoiler = True
    
    component_metadata = ComponentMetadataContainer(
        color = color,
        components = components,
        spoiler = spoiler,
    )
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_ne(copy, component_metadata)
    
    vampytest.assert_eq(copy.color, color)
    vampytest.assert_eq(
        copy.components,
        (
            Component(ComponentType.text_display, content = f'@{user.name_at(guild)}'),
        ),
    )
    vampytest.assert_eq(copy.spoiler, spoiler)


def test__ComponentMetadataContainer__copy():
    """
    Tests whether ``ComponentMetadataContainer.copy`` works as intended.
    """
    color = Color.from_rgb(12, 255, 26)
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    spoiler = True
    
    component_metadata = ComponentMetadataContainer(
        color = color,
        components = components,
        spoiler = spoiler,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataContainer__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataContainer.copy_with`` works as intended.
    
    Case: no fields.
    """
    color = Color.from_rgb(12, 255, 26)
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    spoiler = True
    
    component_metadata = ComponentMetadataContainer(
        color = color,
        components = components,
        spoiler = spoiler,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataContainer__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataContainer.copy_with`` works as intended.
    
    Case: all fields.
    """
    old_color = Color.from_rgb(12, 255, 26)
    old_components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    old_spoiler = True
    
    new_color = Color.from_rgb(12, 17, 26)
    new_components = [
        Component(ComponentType.text_display, content = 'yuina'),
    ]
    new_spoiler = False
    
    component_metadata = ComponentMetadataContainer(
        color = old_color,
        components = old_components,
        spoiler = old_spoiler,
    )
    copy = component_metadata.copy_with(
        color = new_color,
        components = new_components,
        spoiler = new_spoiler,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    
    vampytest.assert_eq(copy.color, new_color)
    vampytest.assert_eq(copy.components, tuple(new_components))
    vampytest.assert_eq(copy.spoiler, new_spoiler)


def test__ComponentMetadataContainer__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataContainer.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields.
    """
    color = Color.from_rgb(12, 255, 26)
    components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    spoiler = True
    
    component_metadata = ComponentMetadataContainer(
        color = color,
        components = components,
        spoiler = spoiler,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataContainer__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataContainer.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields.
    """
    old_color = Color.from_rgb(12, 255, 26)
    old_components = [
        Component(ComponentType.text_display, content = 'chata'),
    ]
    old_spoiler = True
    
    new_color = Color.from_rgb(12, 17, 26)
    new_components = [
        Component(ComponentType.text_display, content = 'yuina'),
    ]
    new_spoiler = False
    
    component_metadata = ComponentMetadataContainer(
        color = old_color,
        components = old_components,
        spoiler = old_spoiler,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'color': new_color,
        'components': new_components,
        'spoiler': new_spoiler,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    
    vampytest.assert_eq(copy.color, new_color)
    vampytest.assert_eq(copy.components, tuple(new_components))
    vampytest.assert_eq(copy.spoiler, new_spoiler)


def _iter_options__iter_contents():
    content_0 = 'chata'
    content_1 = 'important'
    content_2 = 'lie'
    
    color = Color.from_rgb(12, 255, 26)
    components = [
        Component(ComponentType.text_display, content = content_0),
        Component(ComponentType.text_display, content = content_1),
        Component(
            ComponentType.section, components = [
                Component(ComponentType.text_display, content = content_2),
            ],
        ),
    ]
    spoiler = True
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'color': color,
            'components': components,
            'spoiler': spoiler,
        },
        [
            content_0,
            content_1,
            content_2,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataContainer__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataContainer.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataContainer(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
