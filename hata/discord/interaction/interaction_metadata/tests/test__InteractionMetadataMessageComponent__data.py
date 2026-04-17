import vampytest

from ....component import ComponentType, InteractionComponent

from ..message_component import InteractionMetadataMessageComponent

from .test__InteractionMetadataMessageComponent__constructor import _assert_fields_set


def test__InteractionMetadataMessageComponent__from_data():
    """
    Tests whether ``InteractionMetadataMessageComponent.from_data`` works as intended.
    """
    guild_id = 0
    
    component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Inaba',
        values = ['black', 'rock', 'shooter'],
    )
    
    data = {
        'data': component.to_data(),
    }
    
    interaction_metadata = InteractionMetadataMessageComponent.from_data(data, guild_id)
    _assert_fields_set(interaction_metadata)

    vampytest.assert_eq(interaction_metadata.component, component)
    

def test__InteractionMetadataMessageComponent__to_data():
    """
    Tests whether ``InteractionMetadataMessageComponent.to_data`` works as intended.
    """
    guild_id = 202211060046
    
    component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Inaba',
        values = ['black', 'rock', 'shooter'],
    )
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component = component,
    )
    
    vampytest.assert_eq(
        interaction_metadata.to_data(
            defaults = True,
            guild_id = guild_id,
        ),
        {
            'data': component.to_data(defaults = True),
        },
    )
