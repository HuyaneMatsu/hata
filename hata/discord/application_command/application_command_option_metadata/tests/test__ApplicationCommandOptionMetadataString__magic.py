import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..string import ApplicationCommandOptionMetadataString


def test__ApplicationCommandOptionMetadataString__repr():
    """
    Tests whether ``ApplicationCommandOptionMetadataString.__repr__`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    max_length = 10
    min_length = 20
    
    option_metadata = ApplicationCommandOptionMetadataString(
        required = required,
        autocomplete = autocomplete,
        choices = choices,
        max_length = max_length,
        min_length = min_length,
    )
    
    vampytest.assert_instance(repr(option_metadata), str)


def test__ApplicationCommandOptionMetadataString__hash():
    """
    Tests whether ``ApplicationCommandOptionMetadataString.__hash__`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    max_length = 10
    min_length = 20
    
    option_metadata = ApplicationCommandOptionMetadataString(
        required = required,
        autocomplete = autocomplete,
        choices = choices,
        max_length = max_length,
        min_length = min_length,
    )
    
    vampytest.assert_instance(hash(option_metadata), int)


def test__ApplicationCommandOptionMetadataString__eq():
    """
    Tests whether ``ApplicationCommandOptionMetadataString.__eq__`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    max_length = 10
    min_length = 20
    
    keyword_parameters = {
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
        'max_length': max_length,
        'min_length': min_length,
    }
    
    option_metadata = ApplicationCommandOptionMetadataString(**keyword_parameters)
    
    vampytest.assert_eq(option_metadata, option_metadata)
    vampytest.assert_ne(option_metadata, object())
    
    for field_name, field_value in (
        ('required', False),
        ('autocomplete', False),
        ('choices', None),
        ('max_length', 11),
        ('min_length', 12),
    ):
        test_option_metadata = ApplicationCommandOptionMetadataString(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(option_metadata, test_option_metadata)
