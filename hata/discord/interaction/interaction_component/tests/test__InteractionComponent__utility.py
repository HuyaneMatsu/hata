import vampytest

from ....component import ComponentType

from ..interaction_component import InteractionComponent

from .test__InteractionComponent__constructor import _check_is_all_attribute_set


def test__InteractionComponent__copy():
    """
    Tests whether ``InteractionComponent.copy`` works as intended.
    """
    custom_id = 'Worldly'
    components = [InteractionComponent(custom_id = 'flower')]
    type_ = ComponentType.row
    value = 'flower land'
    
    interaction_component = InteractionComponent(
        custom_id = custom_id,
        components = components,
        type_ = type_,
        value = value,
    )
    
    copy = interaction_component.copy()
    _check_is_all_attribute_set(copy)
    vampytest.assert_not_is(interaction_component, copy)
    vampytest.assert_eq(interaction_component, copy)


def test__InteractionComponent__copy_with():
    """
    Tests whether ``InteractionComponent.copy_with`` works as intended.
    
    Case: No fields given.
    """
    custom_id = 'Worldly'
    components = [InteractionComponent(custom_id = 'flower')]
    type_ = ComponentType.row
    value = 'flower land'
    
    interaction_component = InteractionComponent(
        custom_id = custom_id,
        components = components,
        type_ = type_,
        value = value,
    )
    
    copy = interaction_component.copy_with()
    _check_is_all_attribute_set(copy)
    vampytest.assert_not_is(interaction_component, copy)
    vampytest.assert_eq(interaction_component, copy)


def test__InteractionComponent__copy_with__1():
    """
    Tests whether ``InteractionComponent.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_custom_id = 'Worldly'
    new_custom_id = 'START'
    old_components = [InteractionComponent(custom_id = 'flower')]
    new_components = [InteractionComponent(custom_id = 'crazy')]
    old_type = ComponentType.row
    new_type = ComponentType.button
    old_value = 'flower land'
    new_value = 'beats'
    
    interaction_component = InteractionComponent(
        custom_id = old_custom_id,
        components = old_components,
        type_ = old_type,
        value = old_value,
    )
    
    copy = interaction_component.copy_with(
        custom_id = new_custom_id,
        components = new_components,
        type_ = new_type,
        value = new_value,
    )
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_not_is(interaction_component, copy)

    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.components, tuple(new_components))
    vampytest.assert_is(copy.type, new_type)
    vampytest.assert_eq(copy.value, new_value)


def test__InteractionComponent__iter_components():
    """
    Tests whether ``InteractionComponent.iter_components`` works as intended.
    """
    interaction_component_1 = InteractionComponent(custom_id = 'negative')
    interaction_component_2 = InteractionComponent(custom_id = 'number')
    
    for interaction_component, expected_output in (
        (InteractionComponent(components = None), []),
        (InteractionComponent(components = [interaction_component_1]), [interaction_component_1]),
        (
            InteractionComponent(components = [interaction_component_2, interaction_component_1]),
            [interaction_component_2, interaction_component_1]
        ),
    ):
        vampytest.assert_eq([*interaction_component.iter_components()], expected_output)


def test__InteractionComponent__iter_custom_ids_and_values():
    """
    Tests whether ``InteractionComponent.iter_custom_ids_and_values`` works as intended.
    """
    interaction_component_1 = InteractionComponent(custom_id = 'negative', value = 'ho')
    interaction_component_2 = InteractionComponent(custom_id = 'number', value = 'lo')
    interaction_component_3 = InteractionComponent()
    interaction_component_4 = InteractionComponent(
        custom_id = 'enclosed', value = 'dancehall', components = [interaction_component_1, interaction_component_2]
    )
    interaction_component_5 = InteractionComponent(
        components = [interaction_component_1, interaction_component_3]
    )
    
    for interaction_component, expected_output in (
        (interaction_component_1, {'negative': 'ho'}),
        (interaction_component_2, {'number': 'lo'}),
        (interaction_component_3, {}),
        (interaction_component_4, {'negative': 'ho', 'number': 'lo', 'enclosed': 'dancehall'}),
        (interaction_component_5, {'negative': 'ho'}),
    ):
        vampytest.assert_eq(dict(interaction_component.iter_custom_ids_and_values()), expected_output)
