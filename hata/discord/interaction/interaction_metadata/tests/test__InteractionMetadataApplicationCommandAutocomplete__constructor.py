import vampytest

from ...interaction_option import InteractionOption

from ..application_command_autocomplete import InteractionMetadataApplicationCommandAutocomplete


def _assert_fields_set(interaction_metadata):
    """
    Checks whether all fields of the given interaction metadata are set.
    
    Parameters
    ----------
    interaction_metadata : ``InteractionMetadataApplicationCommandAutocomplete``
        The interaction metadata to check.
    """
    vampytest.assert_instance(interaction_metadata, InteractionMetadataApplicationCommandAutocomplete)
    vampytest.assert_instance(interaction_metadata.application_command_id, int)
    vampytest.assert_instance(interaction_metadata.application_command_name, str)
    vampytest.assert_instance(interaction_metadata.options, tuple, nullable = True)


def test__InteractionMetadataApplicationCommandAutocomplete__new__no_fields():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.__new__`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete()
    _assert_fields_set(interaction_metadata)


def test__InteractionMetadataApplicationCommandAutocomplete__new__all_fields():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.__new__`` works as intended.
    
    Case: All fields given.
    """
    application_command_id = 202211060001
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        application_command_id = application_command_id,
        application_command_name = application_command_name,
        options = options,
    )
    _assert_fields_set(interaction_metadata)
    
    vampytest.assert_eq(interaction_metadata.application_command_id, application_command_id)
    vampytest.assert_eq(interaction_metadata.application_command_name, application_command_name)
    vampytest.assert_eq(interaction_metadata.options, tuple(options))


def test__InteractionMetadataApplicationCommandAutocomplete__from_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.from_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete.from_keyword_parameters({})
    _assert_fields_set(interaction_metadata)


def test__InteractionMetadataApplicationCommandAutocomplete__from_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.from_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    application_command_id = 202509140002
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete.from_keyword_parameters({
        'application_command_id': application_command_id,
        'application_command_name': application_command_name,
        'options': options,
    })
    _assert_fields_set(interaction_metadata)
    
    vampytest.assert_eq(interaction_metadata.application_command_id, application_command_id)
    vampytest.assert_eq(interaction_metadata.application_command_name, application_command_name)
    vampytest.assert_eq(interaction_metadata.options, tuple(options))


def test__InteractionMetadataApplicationCommandAutocomplete__create_empty():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete._create_empty`` works as intended.
    """
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete._create_empty()
    _assert_fields_set(interaction_metadata)
