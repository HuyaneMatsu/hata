import vampytest

from ..checkbox import InteractionComponentMetadataCheckbox


def _assert_fields_set(interaction_component_metadata):
    """
    Checks whether the ``InteractionComponentMetadataCheckbox`` has all it's attributes set.
    
    Parameters
    ----------
    interaction_component_metadata : ``InteractionComponentMetadataCheckbox``
        Component metadata to check.
    """
    vampytest.assert_instance(interaction_component_metadata, InteractionComponentMetadataCheckbox)
    vampytest.assert_instance(interaction_component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(interaction_component_metadata.value, str, nullable = True)


def test__InteractionComponentMetadataCheckbox__new__no_fields():
    """
    Tests whether ``InteractionComponentMetadataCheckbox.__new__`` works as intended.
    
    Case: no fields given.
    """
    interaction_component_metadata = InteractionComponentMetadataCheckbox()
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataCheckbox__new__all_fields():
    """
    Tests whether ``InteractionComponentMetadataCheckbox.__new__`` works as intended.
    
    Case: all fields given.
    """
    custom_id = 'koishi'
    value = '\001'
    
    interaction_component_metadata = InteractionComponentMetadataCheckbox(
        custom_id = custom_id,
        value = value,
    )
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.custom_id, custom_id)
    vampytest.assert_eq(interaction_component_metadata.value, value)


def test__InteractionComponentMetadataCheckbox__from_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataCheckbox.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    interaction_component_metadata = InteractionComponentMetadataCheckbox.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataCheckbox__from_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionComponentMetadataCheckbox.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    custom_id = 'koishi'
    value = '\001'
    
    keyword_parameters = {
        'custom_id': custom_id,
        'value': value,
    }
    
    interaction_component_metadata = InteractionComponentMetadataCheckbox.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.custom_id, custom_id)
    vampytest.assert_eq(interaction_component_metadata.value, value)
