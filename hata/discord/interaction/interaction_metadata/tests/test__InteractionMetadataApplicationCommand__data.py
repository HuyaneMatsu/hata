import vampytest

from ....application_command import ApplicationCommandTargetType

from ...interaction_option import InteractionOption

from ..application_command import InteractionMetadataApplicationCommand

from .test__InteractionMetadataApplicationCommand__constructor import _assert_fields_set


def test__InteractionMetadataApplicationCommand__from_data():
    """
    Tests whether ``InteractionMetadataApplicationCommand.from_data`` works as intended.
    """
    guild_id = 0
    application_command_id = 202211060016
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    target_id = 202211060018
    target_type = ApplicationCommandTargetType.user
    
    data = {
        'data': {
            'id': str(application_command_id),
            'name': application_command_name,
            'options': [option.to_data(defaults = True) for option in options],
            'target_id': str(target_id),
            'type': target_type.value,
        },
    }
    
    interaction_metadata = InteractionMetadataApplicationCommand.from_data(data, guild_id)
    _assert_fields_set(interaction_metadata)

    vampytest.assert_eq(interaction_metadata.application_command_id, application_command_id)
    vampytest.assert_eq(interaction_metadata.application_command_name, application_command_name)
    vampytest.assert_eq(interaction_metadata.options, tuple(options))
    vampytest.assert_eq(interaction_metadata.target_id, target_id)
    vampytest.assert_is(interaction_metadata.target_type, target_type)


def test__InteractionMetadataApplicationCommand__to_data():
    """
    Tests whether ``InteractionMetadataApplicationCommand.to_data`` works as intended.
    """
    guild_id = 202211060019
    
    application_command_id = 202211060022
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    target_id = 202211060021
    target_type = ApplicationCommandTargetType.user
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = application_command_id,
        application_command_name = application_command_name,
        options = options,
        target_id = target_id,
        target_type = target_type,
    )
    
    vampytest.assert_eq(
        interaction_metadata.to_data(
            defaults = True,
            guild_id = guild_id,
        ),
        {
            'data': {
                'id': str(application_command_id),
                'name': application_command_name,
                'options': [option.to_data(defaults = True) for option in options],
                'target_id': str(target_id),
                'type': target_type.value,
            },
        },
    )
