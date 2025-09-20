import vampytest

from ....component import ComponentType

from ..interaction_component import InteractionComponent

from .test__InteractionComponent__constructor import _assert_fields_set


def test__InteractionComponent__copy():
    """
    Tests whether ``InteractionComponent.copy`` works as intended.
    """
    custom_id = 'Worldly'
    component_type = ComponentType.text_input
    value = 'flower land'
    
    interaction_component = InteractionComponent(
        component_type,
        custom_id = custom_id,
        value = value,
    )
    
    copy = interaction_component.copy()
    _assert_fields_set(copy)
    vampytest.assert_not_is(interaction_component, copy)
    vampytest.assert_eq(interaction_component, copy)


def test__InteractionComponent__copy_with__no_fields():
    """
    Tests whether ``InteractionComponent.copy_with`` works as intended.
    
    Case: No fields given.
    """
    custom_id = 'Worldly'
    component_type = ComponentType.text_input
    value = 'flower land'
    
    interaction_component = InteractionComponent(
        component_type,
        custom_id = custom_id,
        value = value,
    )
    
    copy = interaction_component.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_not_is(interaction_component, copy)
    vampytest.assert_eq(interaction_component, copy)


def test__InteractionComponent__copy_with__all_fields():
    """
    Tests whether ``InteractionComponent.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_custom_id = 'Worldly'
    old_component_type = ComponentType.text_input
    old_value = 'flower land'
    
    new_custom_id = 'START'
    new_component_type = ComponentType.text_input
    new_value = 'beats'
    
    interaction_component = InteractionComponent(
        old_component_type,
        custom_id = old_custom_id,
        value = old_value,
    )
    
    copy = interaction_component.copy_with(
        custom_id = new_custom_id,
        component_type = new_component_type,
        value = new_value,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(interaction_component, copy)

    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_is(copy.type, new_component_type)
    vampytest.assert_eq(copy.value, new_value)


def _iter_options__iter_components():
    interaction_component_0 = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'negative',
    )
    interaction_component_1 = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'number',
    )
    
    yield (
        InteractionComponent(
            ComponentType.row,
            components = None,
        ),
        [],
    )
    
    yield (
        InteractionComponent(
            ComponentType.row,
            components = [
                interaction_component_0,
            ],
        ),
        [
            interaction_component_0,
        ],
    )
    
    yield (
        InteractionComponent(
            ComponentType.row,
            components = [
                interaction_component_1,
                interaction_component_0,
            ],
        ),
        [
            interaction_component_1,
            interaction_component_0,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_components()).returning_last())
def test__InteractionComponent__iter_components(interaction_component):
    """
    Tests whether ``InteractionComponent.iter_components`` works as intended.
    
    Parameters
    ----------
    interaction_component : ``InteractionComponent``
        Interaction component to test with.
    
    Returns
    -------
    output : `list<InteractionComponent>`
    """
    return [*interaction_component.iter_components()]


def _iter_options__iter_custom_ids_and_values():
    interaction_component_0 = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'negative',
        value = 'kaenbyou',
    )
    interaction_component_1 = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'number',
        values = ['kaenbyou', 'rin'],
    )
    interaction_component_2 = InteractionComponent(
        ComponentType.none,
    )
    interaction_component_3 = InteractionComponent(
        ComponentType.row,
        components = [
            interaction_component_0,
            interaction_component_1,
        ],
    )
    
    yield (
        interaction_component_0,
        [
            ('negative', ComponentType.text_input, 'kaenbyou'),
        ],
    )
    
    yield (
        interaction_component_1,
        [
            ('number', ComponentType.string_select, ('kaenbyou', 'rin')),
        ],
    )
    
    yield (
        interaction_component_2,
        [],
    )
    
    yield (
        interaction_component_3,
        [
            ('negative', ComponentType.text_input, 'kaenbyou'),
            ('number', ComponentType.string_select, ('kaenbyou', 'rin')),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionComponent__iter_custom_ids_and_values(interaction_component):
    """
    Tests whether ``InteractionComponent.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    interaction_component : ``InteractionComponent``
        Interaction component to test with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    return [*interaction_component.iter_custom_ids_and_values()]


def test__InteractionComponent__proxies__read_text_input():
    """
    Tests whether ``InteractionComponent`` field proxies work as intended.
    
    Case: reading text input fields.
    """
    custom_id = 'rabbit'
    value = 'moon'
    
    interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = custom_id,
        value = value
    )
    
    vampytest.assert_eq(interaction_component.custom_id, custom_id)
    vampytest.assert_eq(interaction_component.value, value)


def test__InteractionComponent__proxies__read_string_select():
    """
    Tests whether ``InteractionComponent`` field proxies work as intended.
    
    Case: reading string select fields.
    """
    custom_id = 'rabbit'
    values = ['moon', 'myon']
    
    interaction_component = InteractionComponent(
        ComponentType.string_select,
        custom_id = custom_id,
        values = values
    )
    
    vampytest.assert_eq(interaction_component.custom_id, custom_id)
    vampytest.assert_eq(interaction_component.values, tuple(values))


def test__InteractionComponent__proxies__read_row():
    """
    Tests whether ``InteractionComponent`` field proxies work as intended.
    
    Case: reading row fields.
    """
    nested_interaction_components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'tewi',
        ),
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'eirin',
        ),
    ]
    
    interaction_component = InteractionComponent(
        ComponentType.row,
        components = nested_interaction_components,
    )
    
    vampytest.assert_eq(interaction_component.components, tuple(nested_interaction_components))


def test__InteractionComponent__proxies__read_label():
    """
    Tests whether ``InteractionComponent`` field proxies work as intended.
    
    Case: reading label fields.
    """
    nested_interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'tewi',
    )
    
    interaction_component = InteractionComponent(
        ComponentType.label,
        component = nested_interaction_component,
    )
    
    vampytest.assert_eq(interaction_component.component, nested_interaction_component)


def test__InteractionComponent__proxies__read_section():
    """
    Tests whether ``InteractionComponent`` field proxies work as intended.
    
    Case: reading section fields.
    """
    nested_interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'satori'
    )
    
    interaction_component = InteractionComponent(
        ComponentType.section,
        components = nested_interaction_components,
        thumbnail = thumbnail,
    )
    
    vampytest.assert_eq(interaction_component.components, tuple(nested_interaction_components))
    vampytest.assert_eq(interaction_component.thumbnail, thumbnail)


def test__InteractionComponent__proxies__write_text_input():
    """
    Tests whether ``InteractionComponent`` field proxies work as intended.
    
    Case: writing text input fields.
    """
    custom_id = 'rabbit'
    value = 'moon'
    
    interaction_component = InteractionComponent(
        ComponentType.text_input,
    )
    
    interaction_component.custom_id = custom_id
    interaction_component.value = value
    
    vampytest.assert_eq(interaction_component.custom_id, custom_id)
    vampytest.assert_eq(interaction_component.value, value)


def test__InteractionComponent__proxies__write_string_select():
    """
    Tests whether ``InteractionComponent`` field proxies work as intended.
    
    Case: writing string select fields.
    """
    custom_id = 'rabbit'
    values = ['moon', 'myon']
    
    interaction_component = InteractionComponent(
        ComponentType.string_select,
        custom_id = custom_id,
        values = values
    )
    
    interaction_component.custom_id = custom_id
    interaction_component.values = values
    
    vampytest.assert_eq(interaction_component.custom_id, custom_id)
    vampytest.assert_eq(interaction_component.values, tuple(values))


def test__InteractionComponent__proxies__write_row():
    """
    Tests whether ``InteractionComponent`` field proxies work as intended.
    
    Case: writing row fields.
    """
    nested_interaction_components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'tewi',
        ),
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'eirin',
        ),
    ]
    
    interaction_component = InteractionComponent(
        ComponentType.row,
    )
    
    interaction_component.components = nested_interaction_components
    
    vampytest.assert_eq(interaction_component.components, tuple(nested_interaction_components))


def test__InteractionComponent__proxies__write_label():
    """
    Tests whether ``InteractionComponent`` field proxies work as intended.
    
    Case: writing label fields.
    """
    nested_interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'tewi',
    )
    
    interaction_component = InteractionComponent(
        ComponentType.label,
    )
    
    interaction_component.component = nested_interaction_component
    
    vampytest.assert_eq(interaction_component.component, nested_interaction_component)


def test__InteractionComponent__proxies__write_section():
    """
    Tests whether ``InteractionComponent`` field proxies work as intended.
    
    Case: writing section fields.
    """
    nested_interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'satori'
    )
    
    interaction_component = InteractionComponent(
        ComponentType.section,
    )
    
    interaction_component.components = nested_interaction_components
    interaction_component.thumbnail = thumbnail
    
    vampytest.assert_eq(interaction_component.components, tuple(nested_interaction_components))
    vampytest.assert_eq(interaction_component.thumbnail, thumbnail)
