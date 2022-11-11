import vampytest

from ....component import ComponentType

from ..interaction_component import InteractionComponent


def test__InteractionComponent__repr():
    """
    Tests whether ``InteractionComponent.__repr__`` works as intended.
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
    
    vampytest.assert_instance(repr(interaction_component), str)


def test__InteractionComponent__hash():
    """
    Tests whether ``InteractionComponent.__hash__`` works as intended.
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
    
    vampytest.assert_instance(hash(interaction_component), int)


def test__InteractionComponent__eq():
    """
    Tests whether ``InteractionComponent.__eq__`` works as intended.
    """
    custom_id = 'Worldly'
    components = [InteractionComponent(custom_id = 'flower')]
    type_ = ComponentType.row
    value = 'flower land'
    
    keyword_parameters = {
        'custom_id': custom_id,
        'components': components,
        'type_': type_,
        'value': value,
    }
    
    interaction_component = InteractionComponent(**keyword_parameters)
    
    vampytest.assert_eq(interaction_component, interaction_component)
    vampytest.assert_ne(interaction_component, object())

    for field_custom_id, field_value in (
        ('custom_id', 'Night'),
        ('components', None),
        ('type_', ComponentType.button),
        ('value', 'Blooms'),
    ):
        test_interaction_component = InteractionComponent(**{**keyword_parameters, field_custom_id: field_value})
        vampytest.assert_ne(interaction_component, test_interaction_component)
