import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..row import InteractionComponentMetadataRow

from .test__InteractionComponentMetadataRow__constructor import _assert_fields_set


def test__InteractionComponentMetadataRow__from_data():
    """
    Tests whether ``InteractionComponentMetadataRow.from_data`` works as intended.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'koishi',
        ),
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'smart',
        ),
    ]
    
    data = {
        'components': [interaction_component.to_data() for interaction_component in interaction_components],
    }
    
    interaction_component_metadata = InteractionComponentMetadataRow.from_data(data)
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.components, tuple(interaction_components))


def test__InteractionComponentMetadataRow__to_data():
    """
    Tests whether ``InteractionComponentMetadataRow.to_data`` works as intended.
    
    Case: include defaults.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'koishi',
        ),
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'smart',
        ),
    ]
    
    interaction_component_metadata = InteractionComponentMetadataRow(
        components = interaction_components,
    )
    
    vampytest.assert_eq(
        interaction_component_metadata.to_data(
            defaults = True,
        ),
        {
            'components': [
                interaction_component.to_data(defaults = True) for interaction_component in interaction_components
            ],
        },
    )
