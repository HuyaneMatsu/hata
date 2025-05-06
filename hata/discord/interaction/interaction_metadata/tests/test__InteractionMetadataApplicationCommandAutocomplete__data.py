import vampytest

from ...interaction_option import InteractionOption

from ..application_command_autocomplete import InteractionMetadataApplicationCommandAutocomplete

from .test__InteractionMetadataApplicationCommandAutocomplete__constructor import _assert_fields_set


def test__InteractionMetadataApplicationCommandAutocomplete__from_data():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.from_data`` works as intended.
    """
    guild_id = 0
    application_command_id = 202211060002
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    data = {
        'id': str(application_command_id),
        'name': name,
        'options': [option.to_data(defaults = True) for option in options],
    }
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete.from_data(data, guild_id)
    _assert_fields_set(interaction_metadata)

    vampytest.assert_eq(interaction_metadata.id, application_command_id)
    vampytest.assert_eq(interaction_metadata.name, name)
    vampytest.assert_eq(interaction_metadata.options, tuple(options))
    

def test__InteractionMetadataApplicationCommandAutocomplete__to_data():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.to_data`` works as intended.
    """
    guild_id = 202211060003
    application_command_id = 202211060004
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        application_command_id = application_command_id,
        name = name,
        options = options,
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
        },
    )
