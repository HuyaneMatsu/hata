import vampytest

from ..button import InteractionComponentMetadataButton


def _assert_fields_set(interaction_component_metadata):
    """
    Checks whether the ``InteractionComponentMetadataButton`` has all it's attributes set.
    
    Parameters
    ----------
    interaction_component_metadata : ``InteractionComponentMetadataButton``
        Component metadata to check.
    """
    vampytest.assert_instance(interaction_component_metadata, InteractionComponentMetadataButton)
    vampytest.assert_instance(interaction_component_metadata.custom_id, str, nullable = True)


def test__InteractionComponentMetadataButton__new__no_fields():
    """
    Tests whether ``InteractionComponentMetadataButton.__new__`` works as intended.
    
    Case: no fields given.
    """
    interaction_component_metadata = InteractionComponentMetadataButton()
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataButton__new__all_fields():
    """
    Tests whether ``InteractionComponentMetadataButton.__new__`` works as intended.
    
    Case: all fields given.
    """
    custom_id = 'koishi'
    
    interaction_component_metadata = InteractionComponentMetadataButton(
        custom_id = custom_id,
    )
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.custom_id, custom_id)


def test__InteractionComponentMetadataButton__from_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataButton.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    interaction_component_metadata = InteractionComponentMetadataButton.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataButton__from_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionComponentMetadataButton.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    custom_id = 'koishi'
    
    keyword_parameters = {
        'custom_id': custom_id,
    }
    
    interaction_component_metadata = InteractionComponentMetadataButton.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.custom_id, custom_id)
