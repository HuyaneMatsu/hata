import vampytest

from ..button import InteractionComponentMetadataButton

from .test__InteractionComponentMetadataButton__constructor import _assert_fields_set


def test__InteractionComponentMetadataButton__from_data():
    """
    Tests whether ``InteractionComponentMetadataButton.from_data`` works as intended.
    """
    custom_id = 'koishi'
    
    data = {
        'custom_id': custom_id,
    }
    
    interaction_component_metadata = InteractionComponentMetadataButton.from_data(data)
    _assert_fields_set(interaction_component_metadata)
    
    vampytest.assert_eq(interaction_component_metadata.custom_id, custom_id)


def test__InteractionComponentMetadataButton__to_data():
    """
    Tests whether ``InteractionComponentMetadataButton.to_data`` works as intended.
    
    Case: include defaults.
    """
    custom_id = 'koishi'
    
    interaction_component_metadata = InteractionComponentMetadataButton(
        custom_id = custom_id,
    )
    
    vampytest.assert_eq(
        interaction_component_metadata.to_data(
            defaults = True,
        ),
        {
            'custom_id': custom_id,
        },
    )
