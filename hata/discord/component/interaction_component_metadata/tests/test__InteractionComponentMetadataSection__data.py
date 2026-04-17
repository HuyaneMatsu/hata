import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..section import InteractionComponentMetadataSection

from .test__InteractionComponentMetadataSection__constructor import _assert_fields_set


def test__InteractionComponentMetadataSection__from_data():
    """
    Tests whether ``InteractionComponentMetadataSection.from_data`` works as intended.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'alice',
    )
    
    data = {
        'components': [interaction_component.to_data() for interaction_component in interaction_components],
        'thumbnail': thumbnail.to_data(),
    }
    
    interaction_component_metadata = InteractionComponentMetadataSection.from_data(data)
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.components, tuple(interaction_components))
    vampytest.assert_eq(interaction_component_metadata.thumbnail, thumbnail)


def test__InteractionComponentMetadataSection__to_data():
    """
    Tests whether ``InteractionComponentMetadataSection.to_data`` works as intended.
    
    Case: include defaults.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_display,
        ),
        InteractionComponent(
            ComponentType.text_display,
        ),
    ]
    
    thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'alice',
    )
    
    interaction_component_metadata = InteractionComponentMetadataSection(
        components = interaction_components,
        thumbnail = thumbnail,
    )
    
    vampytest.assert_eq(
        interaction_component_metadata.to_data(
            defaults = True,
        ),
        {
            'components': [
                interaction_component.to_data(defaults = True) for interaction_component in interaction_components
            ],
            'thumbnail': thumbnail.to_data(),
        },
    )
