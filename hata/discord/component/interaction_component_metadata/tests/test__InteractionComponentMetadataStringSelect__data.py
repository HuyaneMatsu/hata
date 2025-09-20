import vampytest

from ..string_select import InteractionComponentMetadataStringSelect

from .test__InteractionComponentMetadataStringSelect__constructor import _assert_fields_set


def test__InteractionComponentMetadataStringSelect__from_data():
    """
    Tests whether ``InteractionComponentMetadataStringSelect.from_data`` works as intended.
    """
    custom_id = 'koishi'
    values = ['oh', 'smart']
    
    data = {
        'custom_id': custom_id,
        'values': values,
    }
    
    interaction_component_metadata = InteractionComponentMetadataStringSelect.from_data(data)
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.custom_id, custom_id)
    vampytest.assert_eq(interaction_component_metadata.values, tuple(values))


def test__InteractionComponentMetadataStringSelect__to_data():
    """
    Tests whether ``InteractionComponentMetadataStringSelect.to_data`` works as intended.
    
    Case: include defaults.
    """
    custom_id = 'koishi'
    values = ['oh', 'smart']
    
    interaction_component_metadata = InteractionComponentMetadataStringSelect(
        custom_id = custom_id,
        values = values,
    )
    
    vampytest.assert_eq(
        interaction_component_metadata.to_data(
            defaults = True,
        ),
        {
            'custom_id': custom_id,
            'values': values,
        },
    )
