import vampytest

from ...component import ComponentType
from ...interaction_component_metadata import InteractionComponentMetadataBase

from ..interaction_component import InteractionComponent


def _assert_fields_set(interaction_component):
    """
    Checks whether all attributes of the given interaction component are set.
    
    Parameters
    ----------
    interaction_component : ``InteractionComponent``
    """
    vampytest.assert_instance(interaction_component, InteractionComponent)
    vampytest.assert_instance(interaction_component.metadata, InteractionComponentMetadataBase)
    vampytest.assert_instance(interaction_component.type, ComponentType)


def test__InteractionComponent__new__no_fields():
    """
    Tests whether ``InteractionComponent.__new__`` works as intended.
    
    Case: No fields.
    """
    interaction_component = InteractionComponent(
        ComponentType.text_input,
    )
    _assert_fields_set(interaction_component)


def test__InteractionComponent__new__all_fields():
    """
    Tests whether ``InteractionComponent.__new__`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'Worldly'
    component_type = ComponentType.text_input
    value = 'flower land'
    
    interaction_component = InteractionComponent(
        component_type,
        custom_id = custom_id,
        value = value,
    )
    _assert_fields_set(interaction_component)
    
    vampytest.assert_eq(interaction_component.custom_id, custom_id)
    vampytest.assert_is(interaction_component.type, component_type)
    vampytest.assert_eq(interaction_component.value, value)


def test__InteractionComponent__create_empty():
    """
    Tests whether ``InteractionComponent._create_empty`` works as intended.
    """
    interaction_component = InteractionComponent._create_empty()
    _assert_fields_set(interaction_component)
