import vampytest

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..nested import ApplicationCommandOptionMetadataNested


def test__ApplicationCommandOptionMetadataNested__repr():
    """
    Tests whether ``ApplicationCommandOptionMetadataNested.__repr__`` works as intended.
    """
    options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    
    option_metadata = ApplicationCommandOptionMetadataNested(
        options = options,
    )
    
    vampytest.assert_instance(repr(option_metadata), str)


def test__ApplicationCommandOptionMetadataNested__hash():
    """
    Tests whether ``ApplicationCommandOptionMetadataNested.__hash__`` works as intended.
    """
    options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    
    option_metadata = ApplicationCommandOptionMetadataNested(
        options = options,
    )
    
    vampytest.assert_instance(hash(option_metadata), int)


def test__ApplicationCommandOptionMetadataNested__eq():
    """
    Tests whether ``ApplicationCommandOptionMetadataNested.__eq__`` works as intended.
    """
    options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    
    keyword_parameters = {
        'options': options,
    }
    
    option_metadata = ApplicationCommandOptionMetadataNested(**keyword_parameters)
    
    vampytest.assert_eq(option_metadata, option_metadata)
    vampytest.assert_ne(option_metadata, object())
    
    for field_name, field_value in (
        ('options', None),
    ):
        test_option_metadata = ApplicationCommandOptionMetadataNested(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(option_metadata, test_option_metadata)
