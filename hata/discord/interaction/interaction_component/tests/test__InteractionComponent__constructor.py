import vampytest

from ....component import ComponentType

from ..interaction_component import InteractionComponent


def _check_is_all_attribute_set(interaction_component):
    """
    Checks whether all attributes of the given interaction component are set.
    
    Parameters
    ----------
    interaction_component : ``InteractionComponent``
    """
    vampytest.assert_instance(interaction_component, InteractionComponent)
    vampytest.assert_instance(interaction_component.custom_id, str, nullable = True)
    vampytest.assert_instance(interaction_component.components, tuple, nullable = True)
    vampytest.assert_instance(interaction_component.type, ComponentType)
    vampytest.assert_instance(interaction_component.value, str, nullable = True)


def test__InteractionComponent__new__0():
    """
    Tests whether ``InteractionComponent.__new__`` works as intended.
    
    Case: No fields.
    """
    interaction_component = InteractionComponent()
    _check_is_all_attribute_set(interaction_component)


def test__InteractionComponent__new__1():
    """
    Tests whether ``InteractionComponent.__new__`` works as intended.
    
    Case: No fields.
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
    _check_is_all_attribute_set(interaction_component)
    
    vampytest.assert_eq(interaction_component.custom_id, custom_id)
    vampytest.assert_eq(interaction_component.components, tuple(components))
    vampytest.assert_is(interaction_component.type, type_)
    vampytest.assert_eq(interaction_component.value, value)


def test__InteractionComponent__create_empty():
    """
    Tests whether ``InteractionComponent._create_empty`` works as intended.
    """
    interaction_component = InteractionComponent._create_empty()
    _check_is_all_attribute_set(interaction_component)
