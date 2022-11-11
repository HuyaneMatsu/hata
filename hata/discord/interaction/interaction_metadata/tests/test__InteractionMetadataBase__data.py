import vampytest

from ...interaction_event import InteractionEvent

from ..base import InteractionMetadataBase

from .test__InteractionMetadataBase__constructor import _check_is_all_field_set


def test__InteractionMetadataBase__from_data():
    """
    Tests whether ``InteractionMetadataBase.from_data`` works as intended.
    """
    data = {}
    
    interaction_event = InteractionEvent()
    interaction_metadata = InteractionMetadataBase.from_data(data, interaction_event)
    _check_is_all_field_set(interaction_metadata)


def test__InteractionMetadataBase__to_data():
    """
    Tests whether ``InteractionMetadataBase.to_data`` works as intended.
    """
    guild_id = 202211060000
    interaction_event = InteractionEvent(guild_id = guild_id)
    
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_eq(
        interaction_metadata.to_data(
            defaults = True,
            interaction_event = interaction_event,
        ),
        {
        },
    )
