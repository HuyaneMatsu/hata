import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..numeric import ApplicationCommandOptionMetadataNumeric


def test__ApplicationCommandOptionMetadataNumeric__repr():
    """
    Tests whether ``ApplicationCommandOptionMetadataNumeric.__repr__`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    max_value = 10
    min_value = 20
    
    option_metadata = ApplicationCommandOptionMetadataNumeric({
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_value': max_value,
        'min_value': min_value,
    })
    
    vampytest.assert_instance(repr(option_metadata), str)


def test__ApplicationCommandOptionMetadataNumeric__hash():
    """
    Tests whether ``ApplicationCommandOptionMetadataNumeric.__hash__`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice("19", 19), ApplicationCommandOptionChoice("18", 18)]
    max_value = 10
    min_value = 20
    
    option_metadata = ApplicationCommandOptionMetadataNumeric({
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_value': max_value,
        'min_value': min_value,
    })
    
    vampytest.assert_instance(hash(option_metadata), int)


def test__ApplicationCommandOptionMetadataNumeric__eq():
    """
    Tests whether ``ApplicationCommandOptionMetadataNumeric.__eq__`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice("19", 19), ApplicationCommandOptionChoice("18", 18)]
    max_value = 10
    min_value = 20
    
    keyword_parameters = {
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_value': max_value,
        'min_value': min_value,
    }
    
    option_metadata = ApplicationCommandOptionMetadataNumeric(keyword_parameters)
    
    vampytest.assert_eq(option_metadata, option_metadata)
    vampytest.assert_ne(option_metadata, object())
    
    for field_name, field_value in (
        ('required', False),
        ('autocomplete', False),
        ('choices', None),
        ('max_value', 11),
        ('min_value', 12),
    ):
        test_option_metadata = ApplicationCommandOptionMetadataNumeric({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(option_metadata, test_option_metadata)
