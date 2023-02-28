import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..float import ApplicationCommandOptionMetadataFloat


def test__ApplicationCommandOptionMetadataFloat__repr():
    """
    Tests whether ``ApplicationCommandOptionMetadataFloat.__repr__`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice("19", 19.0), ApplicationCommandOptionChoice("18", 18.0)]
    max_value = 10.0
    min_value = 20.0
    
    option_metadata = ApplicationCommandOptionMetadataFloat({
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_value': max_value,
        'min_value': min_value,
    })
    
    vampytest.assert_instance(repr(option_metadata), str)


def test__ApplicationCommandOptionMetadataFloat__hash():
    """
    Tests whether ``ApplicationCommandOptionMetadataFloat.__hash__`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice("19", 19.0), ApplicationCommandOptionChoice("18", 18.0)]
    max_value = 10.0
    min_value = 20.0
    
    option_metadata = ApplicationCommandOptionMetadataFloat({
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_value': max_value,
        'min_value': min_value,
    })
    
    vampytest.assert_instance(hash(option_metadata), int)


def test__ApplicationCommandOptionMetadataFloat__eq():
    """
    Tests whether ``ApplicationCommandOptionMetadataFloat.__eq__`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice("19", 19.0), ApplicationCommandOptionChoice("18", 18.0)]
    max_value = 10.0
    min_value = 20.0
    
    keyword_parameters = {
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_value': max_value,
        'min_value': min_value,
    }
    
    option_metadata = ApplicationCommandOptionMetadataFloat(keyword_parameters)
    
    vampytest.assert_eq(option_metadata, option_metadata)
    vampytest.assert_ne(option_metadata, object())
    
    for field_name, field_value in (
        ('required', False),
        ('autocomplete', False),
        ('choices', None),
        ('max_value', 11.0),
        ('min_value', 12.0),
    ):
        test_option_metadata = ApplicationCommandOptionMetadataFloat({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(option_metadata, test_option_metadata)
