import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..section import InteractionComponentMetadataSection


def _assert_fields_set(interaction_component_metadata):
    """
    Checks whether the ``InteractionComponentMetadataSection`` has all it's attributes set.
    
    Parameters
    ----------
    interaction_component_metadata : ``InteractionComponentMetadataSection``
        Component metadata to check.
    """
    vampytest.assert_instance(interaction_component_metadata, InteractionComponentMetadataSection)
    vampytest.assert_instance(interaction_component_metadata.components, tuple, nullable = True)


def test__InteractionComponentMetadataSection__new__no_fields():
    """
    Tests whether ``InteractionComponentMetadataSection.__new__`` works as intended.
    
    Case: no fields given.
    """
    interaction_component_metadata = InteractionComponentMetadataSection()
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataSection__new__all_fields():
    """
    Tests whether ``InteractionComponentMetadataSection.__new__`` works as intended.
    
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
    
    thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'alice',
    )
    
    interaction_component_metadata = InteractionComponentMetadataSection(
        components = interaction_components,
        thumbnail = thumbnail,
    )
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.components, tuple(interaction_components))
    vampytest.assert_eq(interaction_component_metadata.thumbnail, thumbnail)


def test__InteractionComponentMetadataSection__from_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataSection.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    interaction_component_metadata = InteractionComponentMetadataSection.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataSection__from_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionComponentMetadataSection.from_keyword_parameters`` works as intended.
    
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
    
    thumbnail = InteractionComponent(
        ComponentType.button,
        custom_id = 'alice',
    )
    
    keyword_parameters = {
        'components': interaction_components,
        'thumbnail': thumbnail,
    }
    
    interaction_component_metadata = InteractionComponentMetadataSection.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.components, tuple(interaction_components))
    vampytest.assert_eq(interaction_component_metadata.thumbnail, thumbnail)
