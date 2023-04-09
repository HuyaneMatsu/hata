import vampytest

from ....component import ComponentType

from ..interaction_component import InteractionComponent

from .test__InteractionComponent__constructor import _assert_fields_set


def test__InteractionComponent__from_data():
    """
    Tests whether ``InteractionComponent.from_data`` works as intended.
    """
    custom_id = 'Worldly'
    components = [InteractionComponent(custom_id = 'flower')]
    type_ = ComponentType.row
    value = 'flower land'
    
    data = {
        'custom_id': custom_id,
        'components': [component.to_data() for component in components],
        'type': type_.value,
        'value': value,
    }
    
    interaction_component = InteractionComponent.from_data(data)
    _assert_fields_set(interaction_component)
    
    vampytest.assert_eq(interaction_component.custom_id, custom_id)
    vampytest.assert_eq(interaction_component.components, tuple(components))
    vampytest.assert_is(interaction_component.type, type_)
    vampytest.assert_eq(interaction_component.value, value)


def test__InteractionComponent__to_data():
    """
    Tests whether ``InteractionComponent.to_data`` works as intended.
    
    Case: defaults.
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
    
    vampytest.assert_eq(
        interaction_component.to_data(
            defaults = True,
        ),
        {
            'custom_id': custom_id,
            'components': [component.to_data(defaults = True) for component in components],
            'type': type_.value,
            'value': value,
        },
    )
