import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..container import InteractionComponentMetadataContainer

from .test__InteractionComponentMetadataContainer__constructor import _assert_fields_set


def test__InteractionComponentMetadataContainer__copy_with__no_fields():
    """
    Tests whether ``InteractionComponentMetadataContainer.copy_with`` works as intended.
    
    Case: no fields given.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    interaction_component_metadata = InteractionComponentMetadataContainer(
        components = interaction_components,
    )
    
    copy = interaction_component_metadata.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataContainer__copy_with__all_fields():
    """
    Tests whether ``InteractionComponentMetadataContainer.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    new_interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    interaction_component_metadata = InteractionComponentMetadataContainer(
        components = old_interaction_components,
    )
    
    copy = interaction_component_metadata.copy_with(
        components = new_interaction_components,
    )
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_ne(copy, interaction_component_metadata)
    
    vampytest.assert_eq(copy.components, tuple(new_interaction_components))
