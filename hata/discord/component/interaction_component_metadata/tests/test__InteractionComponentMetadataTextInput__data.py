import vampytest

from ..text_input import InteractionComponentMetadataTextInput

from .test__InteractionComponentMetadataTextInput__constructor import _assert_fields_set


def test__InteractionComponentMetadataTextInput__from_data():
    """
    Tests whether ``InteractionComponentMetadataTextInput.from_data`` works as intended.
    """
    custom_id = 'koishi'
    value = 'smart'
    
    data = {
        'custom_id': custom_id,
        'value': value,
    }
    
    interaction_component_metadata = InteractionComponentMetadataTextInput.from_data(data)
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.custom_id, custom_id)
    vampytest.assert_eq(interaction_component_metadata.value, value)


def test__InteractionComponentMetadataTextInput__to_data():
    """
    Tests whether ``InteractionComponentMetadataTextInput.to_data`` works as intended.
    
    Case: include defaults.
    """
    custom_id = 'koishi'
    value = 'smart'
    
    interaction_component_metadata = InteractionComponentMetadataTextInput(
        custom_id = custom_id,
        value = value,
    )
    
    vampytest.assert_eq(
        interaction_component_metadata.to_data(
            defaults = True,
        ),
        {
            'custom_id': custom_id,
            'value': value,
        },
    )
