import vampytest

from ..text_input import InteractionComponentMetadataTextInput


def _assert_fields_set(interaction_component_metadata):
    """
    Checks whether the ``InteractionComponentMetadataTextInput`` has all it's attributes set.
    
    Parameters
    ----------
    interaction_component_metadata : ``InteractionComponentMetadataTextInput``
        Component metadata to check.
    """
    vampytest.assert_instance(interaction_component_metadata, InteractionComponentMetadataTextInput)
    vampytest.assert_instance(interaction_component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(interaction_component_metadata.value, str, nullable = True)


def test__InteractionComponentMetadataTextInput__new__no_fields():
    """
    Tests whether ``InteractionComponentMetadataTextInput.__new__`` works as intended.
    
    Case: no fields given.
    """
    interaction_component_metadata = InteractionComponentMetadataTextInput()
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataTextInput__new__all_fields():
    """
    Tests whether ``InteractionComponentMetadataTextInput.__new__`` works as intended.
    
    Case: all fields given.
    """
    custom_id = 'koishi'
    value = 'smart'
    
    interaction_component_metadata = InteractionComponentMetadataTextInput(
        custom_id = custom_id,
        value = value,
    )
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.custom_id, custom_id)
    vampytest.assert_eq(interaction_component_metadata.value, value)


def test__InteractionComponentMetadataTextInput__from_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataTextInput.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    interaction_component_metadata = InteractionComponentMetadataTextInput.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)


def test__InteractionComponentMetadataTextInput__from_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionComponentMetadataTextInput.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    custom_id = 'koishi'
    value = 'smart'
    
    keyword_parameters = {
        'custom_id': custom_id,
        'value': value,
    }
    
    interaction_component_metadata = InteractionComponentMetadataTextInput.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.custom_id, custom_id)
    vampytest.assert_eq(interaction_component_metadata.value, value)
