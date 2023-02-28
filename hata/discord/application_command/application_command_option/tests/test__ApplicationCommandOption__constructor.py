import vampytest

from ....channel import ChannelType
from ....localization import Locale

from ...application_command_option_choice import ApplicationCommandOptionChoice
from ...application_command_option_metadata import ApplicationCommandOptionMetadataBase

from ..application_command_option import ApplicationCommandOption
from ..preinstanced import ApplicationCommandOptionType


def _assert_fields_set(option):
    """
    Asserts whether every fields of the given application command options are set.
    
    Parameters
    ----------
    option : ``ApplicationCommandOption``
        The application command to check.
    """
    vampytest.assert_instance(option, ApplicationCommandOption)

    vampytest.assert_instance(option.description, str)
    vampytest.assert_instance(option.description_localizations, dict, nullable = True)
    vampytest.assert_instance(option.metadata, ApplicationCommandOptionMetadataBase)
    vampytest.assert_instance(option.name, str)
    vampytest.assert_instance(option.name_localizations, dict, nullable = True)
    vampytest.assert_instance(option.type, ApplicationCommandOptionType)


def test__ApplicationCommandOption__new__string():
    """
    Tests whether ``ApplicationCommandOption.__new__`` works as intended.
    
    Case: string.
    """
    name = 'primrose'
    description = 'flower'
    option_type = ApplicationCommandOptionType.string
    autocomplete = True
    description_localizations = {
        Locale.german: 'hartmann',
    }
    max_length = 30
    min_length = 10
    name_localizations = {
        Locale.german: 'satori',
    }
    required = True
    
    option = ApplicationCommandOption(
        name,
        description,
        option_type,
        autocomplete = autocomplete,
        description_localizations = description_localizations,
        max_length = max_length,
        min_length = min_length,
        name_localizations = name_localizations,
        required = required,
    )
    _assert_fields_set(option)
    
    vampytest.assert_eq(option.name, name)
    vampytest.assert_eq(option.description, description)
    vampytest.assert_is(option.type, option_type)
    vampytest.assert_eq(option.autocomplete, autocomplete)
    vampytest.assert_eq(option.description_localizations, description_localizations)
    vampytest.assert_eq(option.max_length, max_length)
    vampytest.assert_eq(option.min_length, min_length)
    vampytest.assert_eq(option.name_localizations, name_localizations)
    vampytest.assert_eq(option.required, required)


def test__ApplicationCommandOption__new__channel():
    """
    Tests whether ``ApplicationCommandOption.__new__`` works as intended.
    
    Case: channel.
    """
    name = 'primrose'
    description = 'flower'
    option_type = ApplicationCommandOptionType.channel
    channel_types = [ChannelType.private, ChannelType.guild_forum]
    
    option = ApplicationCommandOption(
        name,
        description,
        option_type,
        channel_types = channel_types,
    )
    _assert_fields_set(option)
    
    vampytest.assert_eq(option.name, name)
    vampytest.assert_eq(option.description, description)
    vampytest.assert_is(option.type, option_type)
    vampytest.assert_eq(option.channel_types, tuple(channel_types))


def test__ApplicationCommandOption__new__integer():
    """
    Tests whether ``ApplicationCommandOption.__new__`` works as intended.
    
    Case: integer.
    """
    name = 'primrose'
    description = 'flower'
    option_type = ApplicationCommandOptionType.integer
    min_value = -10
    max_value = +10
    
    option = ApplicationCommandOption(
        name,
        description,
        option_type,
        min_value = min_value,
        max_value = max_value,
    )
    _assert_fields_set(option)
    
    vampytest.assert_eq(option.name, name)
    vampytest.assert_eq(option.description, description)
    vampytest.assert_is(option.type, option_type)
    vampytest.assert_eq(option.min_value, min_value)
    vampytest.assert_eq(option.max_value, max_value)


def test__ApplicationCommandOption__new__float():
    """
    Tests whether ``ApplicationCommandOption.__new__`` works as intended.
    
    Case: float.
    """
    name = 'primrose'
    description = 'flower'
    option_type = ApplicationCommandOptionType.float
    choices = [
        ApplicationCommandOptionChoice('voice', 1.2),
        ApplicationCommandOptionChoice('voice', 2.4),
    ]
    
    option = ApplicationCommandOption(
        name,
        description,
        option_type,
        choices = choices,
    )
    _assert_fields_set(option)
    
    vampytest.assert_eq(option.name, name)
    vampytest.assert_eq(option.description, description)
    vampytest.assert_is(option.type, option_type)
    vampytest.assert_eq(option.choices, tuple(choices))


def test__ApplicationCommandOption__new__sub_command():
    """
    Tests whether ``ApplicationCommandOption.__new__`` works as intended.
    
    Case: sub-command.
    """
    name = 'primrose'
    description = 'flower'
    option_type = ApplicationCommandOptionType.sub_command
    default = True
    options = [
        ApplicationCommandOption('voice-0', 'voice', ApplicationCommandOptionType.string),
        ApplicationCommandOption('voice-1', 'voice', ApplicationCommandOptionType.integer),
    ]
    
    option = ApplicationCommandOption(
        name,
        description,
        option_type,
        default = default,
        options = options,
    )
    _assert_fields_set(option)
    
    vampytest.assert_eq(option.name, name)
    vampytest.assert_eq(option.description, description)
    vampytest.assert_is(option.type, option_type)
    vampytest.assert_eq(option.default, default)
    vampytest.assert_eq(option.options, tuple(options))
