import vampytest

from ....message import Attachment

from ...interaction_event import InteractionEvent
from ...interaction_option import InteractionOption
from ...resolved import Resolved

from ..application_command import InteractionMetadataApplicationCommand

from .test__InteractionMetadataApplicationCommand__constructor import _check_is_all_field_set


def test__InteractionMetadataApplicationCommand__from_data():
    """
    Tests whether ``InteractionMetadataApplicationCommand.from_data`` works as intended.
    """
    id_ = 202211060016
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    resolved = Resolved(attachments = [Attachment.precreate(202211060017)])
    target_id = 202211060018
    
    interaction_event = InteractionEvent()
    
    data = {
        'id': str(id_),
        'name': name,
        'options': [option.to_data(defaults = True) for option in options],
        'resolved': resolved.to_data(defaults = True, interaction_event = interaction_event),
        'target_id': str(target_id),
    }
    
    interaction_metadata = InteractionMetadataApplicationCommand.from_data(data, interaction_event)
    _check_is_all_field_set(interaction_metadata)

    vampytest.assert_eq(interaction_metadata.id, id_)
    vampytest.assert_eq(interaction_metadata.name, name)
    vampytest.assert_eq(interaction_metadata.options, tuple(options))
    vampytest.assert_eq(interaction_metadata.resolved, resolved)
    vampytest.assert_eq(interaction_metadata.target_id, target_id)
    

def test__InteractionMetadataApplicationCommand__to_data():
    """
    Tests whether ``InteractionMetadataApplicationCommand.to_data`` works as intended.
    """
    guild_id = 202211060019
    interaction_event = InteractionEvent(guild_id = guild_id)
    
    id_ = 202211060022
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    resolved = Resolved(attachments = [Attachment.precreate(202211060020)])
    target_id = 202211060021
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        id = id_,
        name = name,
        options = options,
        resolved = resolved,
        target_id = target_id,
    )
    
    vampytest.assert_eq(
        interaction_metadata.to_data(
            defaults = True,
            interaction_event = interaction_event,
        ),
        {
            'id': str(id_),
            'name': name,
            'options': [option.to_data(defaults = True) for option in options],
            'resolved': resolved.to_data(defaults = True, interaction_event = interaction_event),
            'target_id': str(target_id),
        },
    )
