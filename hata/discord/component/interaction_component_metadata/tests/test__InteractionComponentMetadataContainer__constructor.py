import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..container import InteractionComponentMetadataContainer


def _assert_fields_set(interaction_component_metadata):
    """
    Checks whether the ``InteractionComponentMetadataContainer`` has all it's attributes set.
    
    Parameters
    ----------
    interaction_component_metadata : ``InteractionComponentMetadataContainer``
        Component metadata to check.
    """
    vampytest.assert_instance(interaction_component_metadata, InteractionComponentMetadataContainer)
    vampytest.assert_instance(interaction_component_metadata.components, tuple, nullable = True)


def test__InteractionComponentMetadataContainer__new__no_fields():
    """
    Tests whether ``InteractionComponentMetadataContainer.__new__`` works as intended.
    
    Case: no fields given.
    """
    interaction_component_metadata = InteractionComponentMetadataContainer()
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataContainer__new__all_fields():
    """
    Tests whether ``InteractionComponentMetadataContainer.__new__`` works as intended.
    
    Case: all fields given.
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
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.components, tuple(interaction_components))
