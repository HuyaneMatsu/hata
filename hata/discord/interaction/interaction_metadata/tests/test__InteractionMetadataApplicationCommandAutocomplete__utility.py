import vampytest

from ...interaction_option import InteractionOption

from ..application_command_autocomplete import InteractionMetadataApplicationCommandAutocomplete

from .test__InteractionMetadataApplicationCommandAutocomplete__constructor import _assert_fields_set


def test__InteractionMetadataApplicationCommandAutocomplete__copy():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.copy`` works as intended.
    """
    application_command_id = 202211060009
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        application_command_id = application_command_id,
        name = name,
        options = options,
    )
    copy = interaction_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataApplicationCommandAutocomplete__copy_with__0():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.copy_with`` works as intended.
    
    Case: No fields given.
    """
    application_command_id = 202211060010
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        application_command_id = application_command_id,
        name = name,
        options = options,
    )
    copy = interaction_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataApplicationCommandAutocomplete__copy_with__1():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_application_command_id = 202211060011
    old_name = 'Inaba'
    old_options = [InteractionOption(name = 'Rem')]
    
    new_application_command_id = 202211060012
    new_name = 'Reisen'
    new_options = [InteractionOption(name = 'Diablo')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        application_command_id = old_application_command_id,
        name = old_name,
        options = old_options,
    )
    copy = interaction_metadata.copy_with(
        application_command_id = new_application_command_id,
        name = new_name,
        options = new_options,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    
    vampytest.assert_eq(copy.id, new_application_command_id)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.options, tuple(new_options))
