import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..row import InteractionComponentMetadataRow


def _assert_fields_set(interaction_component_metadata):
    """
    Checks whether the ``InteractionComponentMetadataRow`` has all it's attributes set.
    
    Parameters
    ----------
    interaction_component_metadata : ``InteractionComponentMetadataRow``
        Component metadata to check.
    """
    vampytest.assert_instance(interaction_component_metadata, InteractionComponentMetadataRow)
    vampytest.assert_instance(interaction_component_metadata.components, tuple, nullable = True)


def test__InteractionComponentMetadataRow__new__no_fields():
    """
    Tests whether ``InteractionComponentMetadataRow.__new__`` works as intended.
    
    Case: no fields given.
    """
    interaction_component_metadata = InteractionComponentMetadataRow()
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataRow__new__all_fields():
    """
    Tests whether ``InteractionComponentMetadataRow.__new__`` works as intended.
    
    Case: all fields given.
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
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.components, tuple(interaction_components))


def test__InteractionComponentMetadataRow__from_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataRow.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    interaction_component_metadata = InteractionComponentMetadataRow.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataRow__from_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionComponentMetadataRow.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
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
    
    keyword_parameters = {
        'components': interaction_components,
    }
    
    interaction_component_metadata = InteractionComponentMetadataRow.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.components, tuple(interaction_components))
