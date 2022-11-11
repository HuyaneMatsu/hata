import vampytest

from ...interaction_option import InteractionOption

from ..application_command_autocomplete import InteractionMetadataApplicationCommandAutocomplete

from .test__InteractionMetadataApplicationCommandAutocomplete__constructor import _check_is_all_field_set


def test__InteractionMetadataApplicationCommandAutocomplete__copy():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.copy`` works as intended.
    """
    id_ = 202211060009
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        id = id_,
        name = name,
        options = options,
    )
    copy = interaction_metadata.copy()
    _check_is_all_field_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataApplicationCommandAutocomplete__copy_with__0():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.copy_with`` works as intended.
    
    Case: No fields given.
    """
    id_ = 202211060010
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        id = id_,
        name = name,
        options = options,
    )
    copy = interaction_metadata.copy_with()
    _check_is_all_field_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataApplicationCommandAutocomplete__copy_with__1():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_id = 202211060011
    new_id = 202211060012
    old_name = 'Inaba'
    new_name = 'Reisen'
    old_options = [InteractionOption(name = 'Rem')]
    new_options = [InteractionOption(name = 'Diablo')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        id = old_id,
        name = old_name,
        options = old_options,
    )
    copy = interaction_metadata.copy_with(
        id = new_id,
        name = new_name,
        options = new_options,
    )
    _check_is_all_field_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    
    vampytest.assert_eq(copy.id, new_id)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.options, tuple(new_options))
