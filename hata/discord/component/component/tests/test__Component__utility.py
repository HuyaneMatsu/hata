import vampytest

from ....guild import Guild
from ....user import GuildProfile, User

from ...component_metadata import ButtonStyle, TextInputStyle
from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType
from ...media_item import MediaItem
from ...string_select_option import StringSelectOption

from ..component import Component
from ..preinstanced import ComponentType

from .test__Component__constructor import _assert_fields_set


def test__Component__clean_copy():
    """
    Tests whether ``Component.clean_copy`` works as intended.
    """
    guild_id = 202505030040
    guild = Guild.precreate(guild_id)
    
    user_0 = User.precreate(202505030041, name = 'koishi')
    user_0.guild_profiles[guild_id] = GuildProfile(nick = 'koi')
    user_1 = User.precreate(202505030042, name = 'rin')
    user_1.guild_profiles[guild_id] = GuildProfile(nick = 'orin')
    user_2 = User.precreate(202505030043, name = 'utsuho')
    user_2.guild_profiles[guild_id] = GuildProfile(nick = 'okuu')
    
    content_0 = f'{user_0.mention}'
    content_1 = f'{user_1.mention}'
    content_2 = f'{user_2.mention}'
    
    component_type = ComponentType.container
    
    component = Component(
        component_type,
        components = [
            Component(
                ComponentType.section,
                components = [
                    Component(
                        ComponentType.text_display,
                        content = content_0,
                    ),
                ],
            ),
            Component(
                ComponentType.text_display,
                content = content_1,
            ),
            Component(
                ComponentType.section,
                components = [
                    Component(
                        ComponentType.text_display,
                        content = content_2,
                    ),
                ],
            ),
        ],
    )
    
    copy = component.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component)
    vampytest.assert_ne(copy, component)
    
    vampytest.assert_is(copy.type, component_type)
    vampytest.assert_eq(
        copy.components,
        (
            Component(
                ComponentType.section,
                components = [
                    Component(
                        ComponentType.text_display,
                        content = f'@{user_0.name_at(guild)}',
                    ),
                ],
            ),
            Component(
                ComponentType.text_display,
                content = f'@{user_1.name_at(guild)}',
            ),
            Component(
                ComponentType.section,
                components = [
                    Component(
                        ComponentType.text_display,
                        content = f'@{user_2.name_at(guild)}',
                    ),
                ],
            ),
        ),
    )


def test__Component__copy():
    """
    Tests whether ``Component.copy`` works as intended.
    """
    component_type = ComponentType.button
    custom_id = 'chen'
    
    component = Component(component_type, custom_id = custom_id)
    
    copy = component.copy()
    _assert_fields_set(copy)
    vampytest.assert_not_is(component, copy)
    vampytest.assert_is(copy.type, component_type)
    vampytest.assert_is(copy.custom_id, custom_id)


def test__Component__cop_with__no_fields():
    """
    Tests whether ``Component.copy_with`` works as intended.
    
    Case: No fields given.
    """
    component_type = ComponentType.button
    custom_id = 'chen'
    
    component = Component(component_type, custom_id = custom_id)
    
    copy = component.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_not_is(component, copy)
    vampytest.assert_is(copy.type, component_type)
    vampytest.assert_is(copy.custom_id, custom_id)


def test__Component__copy_with__fields():
    """
    Tests whether ``Component.copy_with`` works as intended.
    
    Case: fields given.
    """
    component_type = ComponentType.button
    old_custom_id = 'chen'
    new_custom_id = 'ran'
    
    component = Component(component_type, custom_id = old_custom_id)
    
    copy = component.copy_with(custom_id = new_custom_id)
    _assert_fields_set(copy)
    vampytest.assert_not_is(component, copy)
    vampytest.assert_is(copy.type, component_type)
    vampytest.assert_is(copy.custom_id, new_custom_id)


def _iter_options__iter_components():
    component_0 = Component(ComponentType.button, custom_id = 'chen')
    component_1 = Component(ComponentType.button, custom_id = 'ran')
    
    yield (component_0, [])
    yield (Component(ComponentType.row, components = []), [])
    yield (Component(ComponentType.row, components = [component_0]), [component_0])
    yield (Component(ComponentType.row, components = [component_0, component_1]), [component_0, component_1])
    

@vampytest._(vampytest.call_from(_iter_options__iter_components()).returning_last())
def test__Component__iter_components(input_value):
    """
    Tests whether ``Component.iter_components`` works as intended.
    
    Parameters
    -----------
    input_value : ``Component``
        Component to test with.
    
    Returns
    -------
    output : list<Component>`
    """
    return [*input_value.iter_components()]


def _iter_options__iter_options():
    option_0 = StringSelectOption('yume')
    option_1 = StringSelectOption('ame')
    
    yield Component(ComponentType.string_select), []
    yield Component(ComponentType.string_select, options = [option_0]), [option_0]
    yield Component(ComponentType.string_select, options = [option_0, option_1]), [option_0, option_1]


@vampytest._(vampytest.call_from(_iter_options__iter_options()).returning_last())
def test__Component__iter_options(input_value):
    """
    Tests whether ``Component.iter_options`` works as intended.
    
    Parameters
    -----------
    input_value : ``Component``
        Component to test with.
    
    Returns
    -------
    output : list<StringSelectOption>`
    """
    return [*input_value.iter_options()]


def _iter_options__iter_items():
    item_0 = MediaItem('https://orindance.party/')
    item_1 = MediaItem('https://www.astil.dev/')
    
    yield Component(ComponentType.media_gallery), []
    yield Component(ComponentType.media_gallery, items = [item_0]), [item_0]
    yield Component(ComponentType.media_gallery, items = [item_0, item_1]), [item_0, item_1]


@vampytest._(vampytest.call_from(_iter_options__iter_items()).returning_last())
def test__Component__iter_items(input_value):
    """
    Tests whether ``Component.iter_items`` works as intended.
    
    Parameters
    -----------
    input_value : ``Component``
        Component to test with.
    
    Returns
    -------
    output : list<MediaItem>`
    """
    return [*input_value.iter_items()]


def _iter_options__iter_default_values():
    default_value_0 = EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130051)
    default_value_1 = EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130052)
    
    yield Component(ComponentType.user_select), []
    yield Component(ComponentType.user_select, default_values = [default_value_0]), [default_value_0]
    yield (
        Component(ComponentType.user_select, default_values = [default_value_0, default_value_1]),
        [default_value_0, default_value_1],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_default_values()).returning_last())
def test__Component__iter_default_values(input_value):
    """
    Tests whether ``Component.iter_default_values`` works as intended.
    
    Parameters
    -----------
    input_value : ``Component``
        Component to test with.
    
    Returns
    -------
    output : list<EntitySelectDefaultValue>`
    """
    return [*input_value.iter_default_values()]


def _iter_options__style__read():
    yield Component(ComponentType.string_select), None
    yield Component(ComponentType.button, button_style = ButtonStyle.red), ButtonStyle.red
    yield Component(ComponentType.text_input, text_input_style = TextInputStyle.paragraph), TextInputStyle.paragraph


@vampytest._(vampytest.call_from(_iter_options__style__read()).returning_last())
def test__Component__style__read(input_value):
    """
    Tests whether ``Component.style`` works as intended.
    
    Case: reading.
    
    Parameters
    -----------
    input_value : ``Component``
        Component to test with.
    
    Returns
    -------
    output : `None | PreinstancedBase`
    """
    return input_value.style


def _iter_options__style__write():
    yield Component(ComponentType.button), ButtonStyle.red, 'button_style', ButtonStyle.red
    yield Component(ComponentType.text_input), TextInputStyle.paragraph, 'text_input_style', TextInputStyle.paragraph


@vampytest._(vampytest.call_from(_iter_options__style__write()).returning_last())
def test__Component__style__write(input_value, value, attribute_name):
    """
    Tests whether ``Component.style`` works as intended.
    
    Case: writing.
    
    Parameters
    -----------
    input_value : ``Component``
        Component to test with.
    value : ``PreinstancedBase``
        Value to set as style.
    attribute_name : `str`
        The attribute's name to read.
    
    Returns
    -------
    output : ``PreinstancedBase``
    """
    component = input_value.copy()
    component.style = value
    return getattr(component, attribute_name)


def _iter_options__iter_contents():
    content_0 = 'yukari'
    content_1 = 'chen'
    content_2 = 'ran'
    
    yield (
        {
            'component_type': ComponentType.button,
            'label': 'pop',
        },
        [],
    )
    
    yield (
        {
            'component_type': ComponentType.text_display,
            'content': content_0,
        },
        [
            content_0,
        ],
    )
    
    yield (
        {
            'component_type': ComponentType.container,
            'components': [
                Component(
                    ComponentType.section,
                    components = [
                        Component(
                            ComponentType.text_display,
                            content = content_0,
                        ),
                    ],
                ),
                Component(
                    ComponentType.text_display,
                    content = content_1,
                ),
                Component(
                    ComponentType.section,
                    components = [
                        Component(
                            ComponentType.text_display,
                            content = content_2,
                        ),
                    ],
                ),
            ],
        },
        [
            content_0,
            content_1,
            content_2,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__Component__iter_contents(keyword_parameters):
    """
    Tests whether ``Component.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component = Component(**keyword_parameters)
    
    output = [*component.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__Component__contents(keyword_parameters):
    """
    Tests whether ``Component.contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component = Component(**keyword_parameters)
    
    output = component.contents
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__Component__iter_contents(keyword_parameters):
    """
    Tests whether ``Component.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component = Component(**keyword_parameters)
    
    output = [*component.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
