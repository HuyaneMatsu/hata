import vampytest

from ...interaction_event import InteractionEvent
from ...interaction_component import InteractionComponent

from ..form_submit import InteractionMetadataFormSubmit

from .test__InteractionMetadataFormSubmit__constructor import _check_is_all_field_set


def test__InteractionMetadataFormSubmit__from_data():
    """
    Tests whether ``InteractionMetadataFormSubmit.from_data`` works as intended.
    """
    custom_id = 'Inaba'
    components = [InteractionComponent(custom_id = 'Rem')]
    
    data = {
        'custom_id': custom_id,
        'components': [component.to_data(defaults = True) for component in components],
    }
    
    interaction_event = InteractionEvent()
    interaction_metadata = InteractionMetadataFormSubmit.from_data(data, interaction_event)
    _check_is_all_field_set(interaction_metadata)

    vampytest.assert_eq(interaction_metadata.custom_id, custom_id)
    vampytest.assert_eq(interaction_metadata.components, tuple(components))
    

def test__InteractionMetadataFormSubmit__to_data():
    """
    Tests whether ``InteractionMetadataFormSubmit.to_data`` works as intended.
    """
    guild_id = 202211060003
    interaction_event = InteractionEvent(guild_id = guild_id)
    
    custom_id = 'Inaba'
    components = [InteractionComponent(custom_id = 'Rem')]
    
    interaction_metadata = InteractionMetadataFormSubmit(
        custom_id = custom_id,
        components = components,
    )
    
    vampytest.assert_eq(
        interaction_metadata.to_data(
            defaults = True,
            interaction_event = interaction_event,
        ),
        {
            'custom_id': custom_id,
            'components': [component.to_data(defaults = True) for component in components],
        },
    )
