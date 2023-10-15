import vampytest

from ....component import ComponentType

from ..interaction_component import InteractionComponent

from .test__InteractionComponent__constructor import _assert_fields_set


def test__InteractionComponent__copy():
    """
    Tests whether ``InteractionComponent.copy`` works as intended.
    """
    custom_id = 'Worldly'
    components = [InteractionComponent(custom_id = 'flower')]
    component_type = ComponentType.row
    value = 'flower land'
    
    interaction_component = InteractionComponent(
        custom_id = custom_id,
        components = components,
        component_type = component_type,
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
    components = [InteractionComponent(custom_id = 'flower')]
    component_type = ComponentType.row
    value = 'flower land'
    
    interaction_component = InteractionComponent(
        custom_id = custom_id,
        components = components,
        component_type = component_type,
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
    old_components = [InteractionComponent(custom_id = 'flower')]
    old_type = ComponentType.row
    old_value = 'flower land'
    
    new_custom_id = 'START'
    new_components = [InteractionComponent(custom_id = 'crazy')]
    new_type = ComponentType.button
    new_value = 'beats'
    
    interaction_component = InteractionComponent(
        custom_id = old_custom_id,
        components = old_components,
        component_type = old_type,
        value = old_value,
    )
    
    copy = interaction_component.copy_with(
        custom_id = new_custom_id,
        components = new_components,
        component_type = new_type,
        value = new_value,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(interaction_component, copy)

    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.components, tuple(new_components))
    vampytest.assert_is(copy.type, new_type)
    vampytest.assert_eq(copy.value, new_value)


def _iter_options__iter_components():
    interaction_component_0 = InteractionComponent(custom_id = 'negative')
    interaction_component_1 = InteractionComponent(custom_id = 'number')
    
    yield (InteractionComponent(components = None), [])
    yield (InteractionComponent(components = [interaction_component_0]), [interaction_component_0])
    yield (
        InteractionComponent(components = [interaction_component_1, interaction_component_0]),
        [interaction_component_1, interaction_component_0],
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
    interaction_component_0 = InteractionComponent(custom_id = 'negative', value = 'ho')
    interaction_component_1 = InteractionComponent(custom_id = 'number', value = 'lo')
    interaction_component_2 = InteractionComponent()
    interaction_component_3 = InteractionComponent(
        custom_id = 'enclosed', value = 'dancehall', components = [interaction_component_0, interaction_component_1]
    )
    interaction_component_4 = InteractionComponent(
        components = [interaction_component_0, interaction_component_2]
    )
    
    yield interaction_component_0, {'negative': 'ho'}
    yield interaction_component_1, {'number': 'lo'}
    yield interaction_component_2, {}
    yield interaction_component_3, {'negative': 'ho', 'number': 'lo', 'enclosed': 'dancehall'}
    yield interaction_component_4, {'negative': 'ho'}
    

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
    output : `dict<str, str>`
    """
    return dict(interaction_component.iter_custom_ids_and_values())
