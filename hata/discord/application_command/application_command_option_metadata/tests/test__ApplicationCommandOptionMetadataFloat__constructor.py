import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..float import ApplicationCommandOptionMetadataFloat


def _asert_fields_set(option_metadata):
    """
    Asserts whether all attributes of the application command option metadata are set.
    
    Parameters
    ----------
    option_metadata : ``ApplicationCommandOptionMetadataFloat``
        The application command option metadata to check.
    """
    vampytest.assert_instance(option_metadata, ApplicationCommandOptionMetadataFloat)
    
    vampytest.assert_instance(option_metadata.required, bool)
    vampytest.assert_instance(option_metadata.autocomplete, bool)
    vampytest.assert_instance(option_metadata.choices, tuple, nullable = True)
    vampytest.assert_instance(option_metadata.max_value, float, nullable = True)
    vampytest.assert_instance(option_metadata.min_value, float, nullable = True)


def test__ApplicationCommandOptionMetadataFloat__new__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataFloat.__new__`` works as intended.
    
    Case: No fields given.
    """
    option_metadata = ApplicationCommandOptionMetadataFloat()
    _asert_fields_set(option_metadata)


def test__ApplicationCommandOptionMetadataFloat__new__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataFloat.__new__`` works as intended.
    
    Case: All fields given.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('19', 19.0), ApplicationCommandOptionChoice('18', 18.0)]
    max_value = 10.0
    min_value = 20.0
    
    option_metadata = ApplicationCommandOptionMetadataFloat(
        required = required,
        autocomplete = autocomplete,
        choices = choices,
        max_value = max_value,
        min_value = min_value,
    )
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.required, required)
    vampytest.assert_eq(option_metadata.autocomplete, autocomplete)
    vampytest.assert_eq(option_metadata.choices, tuple(choices))
    vampytest.assert_eq(option_metadata.max_value, max_value)
    vampytest.assert_eq(option_metadata.min_value, min_value)



def test__ApplicationCommandOptionMetadataFloat__from_keyword_parameters__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataFloat.from_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    option_metadata = ApplicationCommandOptionMetadataFloat.from_keyword_parameters({})
    _asert_fields_set(option_metadata)


def test__ApplicationCommandOptionMetadataFloat__from_keyword_parameters__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataFloat.from_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('19', 19.0), ApplicationCommandOptionChoice('18', 18.0)]
    max_value = 10.0
    min_value = 20.0
    
    option_metadata = ApplicationCommandOptionMetadataFloat.from_keyword_parameters({
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_value': max_value,
        'min_value': min_value,
    })
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.required, required)
    vampytest.assert_eq(option_metadata.autocomplete, autocomplete)
    vampytest.assert_eq(option_metadata.choices, tuple(choices))
    vampytest.assert_eq(option_metadata.max_value, max_value)
    vampytest.assert_eq(option_metadata.min_value, min_value)
