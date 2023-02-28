import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..integer import ApplicationCommandOptionMetadataInteger


def test__ApplicationCommandOptionMetadataInteger__repr():
    """
    Tests whether ``ApplicationCommandOptionMetadataInteger.__repr__`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice("19", 19), ApplicationCommandOptionChoice("18", 18)]
    max_value = 10
    min_value = 20
    
    option_metadata = ApplicationCommandOptionMetadataInteger({
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_value': max_value,
        'min_value': min_value,
    })
    
    vampytest.assert_instance(repr(option_metadata), str)


def test__ApplicationCommandOptionMetadataInteger__hash():
    """
    Tests whether ``ApplicationCommandOptionMetadataInteger.__hash__`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice("19", 19), ApplicationCommandOptionChoice("18", 18)]
    max_value = 10
    min_value = 20
    
    option_metadata = ApplicationCommandOptionMetadataInteger({
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_value': max_value,
        'min_value': min_value,
    })
    
    vampytest.assert_instance(hash(option_metadata), int)


def test__ApplicationCommandOptionMetadataInteger__eq():
    """
    Tests whether ``ApplicationCommandOptionMetadataInteger.__eq__`` works as intended.
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
    
    option_metadata = ApplicationCommandOptionMetadataInteger(keyword_parameters)
    
    vampytest.assert_eq(option_metadata, option_metadata)
    vampytest.assert_ne(option_metadata, object())
    
    for field_name, field_value in (
        ('required', False),
        ('autocomplete', False),
        ('choices', None),
        ('max_value', 11),
        ('min_value', 12),
    ):
        test_option_metadata = ApplicationCommandOptionMetadataInteger({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(option_metadata, test_option_metadata)
