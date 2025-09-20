import vampytest

from ...interaction_component import InteractionComponent

from ..base import InteractionComponentMetadataBase


def test__InteractionComponentMetadataBase__placeholders():
    """
    Tests whether ``InteractionComponentMetadataBase``'s placeholders works as intended.
    """
    interaction_component_metadata = InteractionComponentMetadataBase()
    
    vampytest.assert_instance(interaction_component_metadata.component, InteractionComponent, nullable = True)
    vampytest.assert_instance(interaction_component_metadata.components, tuple, nullable = True)
    vampytest.assert_instance(interaction_component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(interaction_component_metadata.thumbnail, InteractionComponent, nullable = True)
    vampytest.assert_instance(interaction_component_metadata.value, str, nullable = True)
    vampytest.assert_instance(interaction_component_metadata.values, str, nullable = True)
