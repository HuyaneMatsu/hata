import vampytest

from ....application_command import ApplicationCommandTargetType
from ....message import Attachment

from ...interaction_option import InteractionOption
from ...resolved import Resolved

from ..application_command import InteractionMetadataApplicationCommand

from .test__InteractionMetadataApplicationCommand__constructor import _check_is_all_field_set


def test__InteractionMetadataApplicationCommand__from_data():
    """
    Tests whether ``InteractionMetadataApplicationCommand.from_data`` works as intended.
    """
    guild_id = 0
    application_command_id = 202211060016
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    resolved = Resolved(attachments = [Attachment.precreate(202211060017)])
    target_id = 202211060018
    target_type = ApplicationCommandTargetType.user
    
    data = {
        'id': str(application_command_id),
        'name': name,
        'options': [option.to_data(defaults = True) for option in options],
        'resolved': resolved.to_data(defaults = True, guild_id = guild_id),
        'target_id': str(target_id),
        'type': target_type.value,
    }
    
    interaction_metadata = InteractionMetadataApplicationCommand.from_data(data, guild_id)
    _check_is_all_field_set(interaction_metadata)

    vampytest.assert_eq(interaction_metadata.id, application_command_id)
    vampytest.assert_eq(interaction_metadata.name, name)
    vampytest.assert_eq(interaction_metadata.options, tuple(options))
    vampytest.assert_eq(interaction_metadata.resolved, resolved)
    vampytest.assert_eq(interaction_metadata.target_id, target_id)
    vampytest.assert_is(interaction_metadata.target_type, target_type)


def test__InteractionMetadataApplicationCommand__to_data():
    """
    Tests whether ``InteractionMetadataApplicationCommand.to_data`` works as intended.
    """
    guild_id = 202211060019
    
    application_command_id = 202211060022
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    resolved = Resolved(attachments = [Attachment.precreate(202211060020)])
    target_id = 202211060021
    target_type = ApplicationCommandTargetType.user
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = application_command_id,
        name = name,
        options = options,
        resolved = resolved,
        target_id = target_id,
        target_type = target_type,
    )
    
    vampytest.assert_eq(
        interaction_metadata.to_data(
            defaults = True,
            guild_id = guild_id,
        ),
        {
            'id': str(application_command_id),
            'name': name,
            'options': [option.to_data(defaults = True) for option in options],
            'resolved': resolved.to_data(defaults = True, guild_id = guild_id),
            'target_id': str(target_id),
            'type': target_type.value,
        },
    )
