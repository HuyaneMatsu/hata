import vampytest

from ..checkbox import InteractionComponentMetadataCheckbox

from .test__InteractionComponentMetadataCheckbox__constructor import _assert_fields_set


def test__InteractionComponentMetadataCheckbox__from_data():
    """
    Tests whether ``InteractionComponentMetadataCheckbox.from_data`` works as intended.
    """
    custom_id = 'koishi'
    value = '\01'
    
    data = {
        'custom_id': custom_id,
        'value': (value == '\01'),
    }
    
    interaction_component_metadata = InteractionComponentMetadataCheckbox.from_data(data)
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.custom_id, custom_id)
    vampytest.assert_eq(interaction_component_metadata.value, value)


def test__InteractionComponentMetadataCheckbox__to_data():
    """
    Tests whether ``InteractionComponentMetadataCheckbox.to_data`` works as intended.
    
    Case: include defaults.
    """
    custom_id = 'koishi'
    value = '\01'
    
    interaction_component_metadata = InteractionComponentMetadataCheckbox(
        custom_id = custom_id,
        value = value,
    )
    
    vampytest.assert_eq(
        interaction_component_metadata.to_data(
            defaults = True,
        ),
        {
            'custom_id': custom_id,
            'value': (value == '\01'),
        },
    )
