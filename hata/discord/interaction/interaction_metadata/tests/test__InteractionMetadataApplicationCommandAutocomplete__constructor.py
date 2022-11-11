import vampytest

from ...interaction_option import InteractionOption

from ..application_command_autocomplete import InteractionMetadataApplicationCommandAutocomplete


def _check_is_all_field_set(interaction_metadata):
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
    _check_is_all_field_set(interaction_metadata)


def test__InteractionMetadataApplicationCommandAutocomplete__new__1():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.__new__`` works as intended.
    
    Case: All fields given.
    """
    id_ = 202211060001
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        id = id_,
        name = name,
        options = options,
    )
    _check_is_all_field_set(interaction_metadata)
    
    vampytest.assert_eq(interaction_metadata.id, id_)
    vampytest.assert_eq(interaction_metadata.name, name)
    vampytest.assert_eq(interaction_metadata.options, tuple(options))
    

def test__InteractionMetadataApplicationCommandAutocomplete__create_empty():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete._create_empty`` works as intended.
    """
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete._create_empty()
    _check_is_all_field_set(interaction_metadata)
