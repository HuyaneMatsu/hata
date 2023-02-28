import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..primitive import ApplicationCommandOptionMetadataPrimitive


def _asert_fields_set(option_metadata):
    """
    Asserts whether all attributes of the application command option metadata are set.
    
    Parameters
    ----------
    option_metadata : ``ApplicationCommandOptionMetadataPrimitive``
        The application command option metadata to check.
    """
    vampytest.assert_instance(option_metadata, ApplicationCommandOptionMetadataPrimitive)
    
    vampytest.assert_instance(option_metadata.required, bool)
    vampytest.assert_instance(option_metadata.autocomplete, bool)
    vampytest.assert_instance(option_metadata.choices, tuple, nullable = True)


def test__ApplicationCommandOptionMetadataPrimitive__new__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataPrimitive.__new__`` works as intended.
    
    Case: No fields given.
    """
    option_metadata = ApplicationCommandOptionMetadataPrimitive({})
    _asert_fields_set(option_metadata)


def test__ApplicationCommandOptionMetadataPrimitive__new__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataPrimitive.__new__`` works as intended.
    
    Case: All fields given.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    
    option_metadata = ApplicationCommandOptionMetadataPrimitive({
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
    })
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.required, required)
    vampytest.assert_eq(option_metadata.autocomplete, autocomplete)
    vampytest.assert_eq(option_metadata.choices, tuple(choices))
