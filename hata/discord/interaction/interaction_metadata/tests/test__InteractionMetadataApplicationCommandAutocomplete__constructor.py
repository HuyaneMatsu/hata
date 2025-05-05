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
    vampytest.assert_instance(interaction_metadata.id, int)
    vampytest.assert_instance(interaction_metadata.name, str)
    vampytest.assert_instance(interaction_metadata.options, tuple, nullable = True)


def test__InteractionMetadataApplicationCommandAutocomplete__new__0():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.__new__`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete()
    _assert_fields_set(interaction_metadata)


def test__InteractionMetadataApplicationCommandAutocomplete__new__1():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.__new__`` works as intended.
    
    Case: All fields given.
    """
    application_command_id = 202211060001
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        application_command_id = application_command_id,
        name = name,
        options = options,
    )
    _assert_fields_set(interaction_metadata)
    
    vampytest.assert_eq(interaction_metadata.id, application_command_id)
    vampytest.assert_eq(interaction_metadata.name, name)
    vampytest.assert_eq(interaction_metadata.options, tuple(options))
    

def test__InteractionMetadataApplicationCommandAutocomplete__create_empty():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete._create_empty`` works as intended.
    """
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete._create_empty()
    _assert_fields_set(interaction_metadata)
