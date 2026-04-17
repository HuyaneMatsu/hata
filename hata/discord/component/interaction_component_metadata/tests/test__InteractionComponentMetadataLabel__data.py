import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..label import InteractionComponentMetadataLabel

from .test__InteractionComponentMetadataLabel__constructor import _assert_fields_set


def test__InteractionComponentMetadataLabel__from_data():
    """
    Tests whether ``InteractionComponentMetadataLabel.from_data`` works as intended.
    """
    interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'koishi',
    )
    
    data = {
        'component': interaction_component.to_data(),
    }
    
    interaction_component_metadata = InteractionComponentMetadataLabel.from_data(data)
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.component, interaction_component)


def test__InteractionComponentMetadataLabel__to_data():
    """
    Tests whether ``InteractionComponentMetadataLabel.to_data`` works as intended.
    
    Case: include defaults.
    """
    interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'koishi',
    )
    
    interaction_component_metadata = InteractionComponentMetadataLabel(
        component = interaction_component,
    )
    
    vampytest.assert_eq(
        interaction_component_metadata.to_data(
            defaults = True,
        ),
        {
            'component': interaction_component.to_data(defaults = True),
        },
    )
