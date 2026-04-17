import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..label import InteractionComponentMetadataLabel


def _assert_fields_set(interaction_component_metadata):
    """
    Checks whether the ``InteractionComponentMetadataLabel`` has all it's attributes set.
    
    Parameters
    ----------
    interaction_component_metadata : ``InteractionComponentMetadataLabel``
        Component metadata to check.
    """
    vampytest.assert_instance(interaction_component_metadata, InteractionComponentMetadataLabel)
    vampytest.assert_instance(interaction_component_metadata.component, InteractionComponent, nullable = True)


def test__InteractionComponentMetadataLabel__new__no_fields():
    """
    Tests whether ``InteractionComponentMetadataLabel.__new__`` works as intended.
    
    Case: no fields given.
    """
    interaction_component_metadata = InteractionComponentMetadataLabel()
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataLabel__new__all_fields():
    """
    Tests whether ``InteractionComponentMetadataLabel.__new__`` works as intended.
    
    Case: all fields given.
    """
    interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'koishi',
    )
    
    interaction_component_metadata = InteractionComponentMetadataLabel(
        component = interaction_component,
    )
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.component, interaction_component)


def test__InteractionComponentMetadataLabel__from_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataLabel.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    interaction_component_metadata = InteractionComponentMetadataLabel.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataLabel__from_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionComponentMetadataLabel.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'koishi',
    )
    
    keyword_parameters = {
        'component': interaction_component,
    }
    
    interaction_component_metadata = InteractionComponentMetadataLabel.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.component, interaction_component)
