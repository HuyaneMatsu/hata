import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..primitive import ApplicationCommandOptionMetadataPrimitive


def test__ApplicationCommandOptionMetadataPrimitive__repr():
    """
    Tests whether ``ApplicationCommandOptionMetadataPrimitive.__repr__`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    
    option_metadata = ApplicationCommandOptionMetadataPrimitive(
        required = required,
        autocomplete = autocomplete,
        choices = choices,
    )
    
    vampytest.assert_instance(repr(option_metadata), str)


def test__ApplicationCommandOptionMetadataPrimitive__hash():
    """
    Tests whether ``ApplicationCommandOptionMetadataPrimitive.__hash__`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    
    option_metadata = ApplicationCommandOptionMetadataPrimitive(
        required = required,
        autocomplete = autocomplete,
        choices = choices,
    )
    
    vampytest.assert_instance(hash(option_metadata), int)


def test__ApplicationCommandOptionMetadataPrimitive__eq():
    """
    Tests whether ``ApplicationCommandOptionMetadataPrimitive.__eq__`` works as intended.
    """
    required = True
    autocomplete = True
    choices = [ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionChoice('suwako')]
    
    keyword_parameters = {
        'required': required,
        'autocomplete': autocomplete,
        'choices': choices,
    }
    
    option_metadata = ApplicationCommandOptionMetadataPrimitive(**keyword_parameters)
    
    vampytest.assert_eq(option_metadata, option_metadata)
    vampytest.assert_ne(option_metadata, object())
    
    for field_name, field_value in (
        ('required', False),
        ('autocomplete', False),
        ('choices', None),
    ):
        test_option_metadata = ApplicationCommandOptionMetadataPrimitive(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(option_metadata, test_option_metadata)
