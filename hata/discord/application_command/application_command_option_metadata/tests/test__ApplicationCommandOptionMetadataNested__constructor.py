import vampytest

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..nested import ApplicationCommandOptionMetadataNested


def _asert_fields_set(option_metadata):
    """
    Asserts whether all attributes of the application command option metadata are set.
    
    Parameters
    ----------
    option_metadata : ``ApplicationCommandOptionMetadataNested``
        The application command option metadata to check.
    """
    vampytest.assert_instance(option_metadata, ApplicationCommandOptionMetadataNested)
    
    vampytest.assert_instance(option_metadata.options, tuple, nullable = True)


def test__ApplicationCommandOptionMetadataNested__new__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataNested.__new__`` works as intended.
    
    Case: No fields given.
    """
    option_metadata = ApplicationCommandOptionMetadataNested({})
    _asert_fields_set(option_metadata)


def test__ApplicationCommandOptionMetadataNested__new__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataNested.__new__`` works as intended.
    
    Case: All fields given.
    """
    options = [
        ApplicationCommandOption('nue', 'nue', ApplicationCommandOptionType.string),
        ApplicationCommandOption('seija', 'seija', ApplicationCommandOptionType.integer),
    ]
    
    option_metadata = ApplicationCommandOptionMetadataNested({
        'options': options,
    })
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.options, tuple(options))
