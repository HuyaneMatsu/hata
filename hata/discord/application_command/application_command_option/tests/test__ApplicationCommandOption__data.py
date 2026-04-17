import vampytest


from ....channel import ChannelType
from ....localization import Locale

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..application_command_option import ApplicationCommandOption
from ..preinstanced import ApplicationCommandOptionType

from .test__ApplicationCommandOption__constructor import _assert_fields_set


def test__ApplicationCommandOption__constructor__from_data():
    """
    Tests whether ``ApplicationCommandOption.from_data`` works as intended.
    """
    description = 'primrose'
    description_localizations = {
        Locale.german: 'hartmann',
    }
    name = 'flower'
    name_localizations = {
        Locale.german: 'satori',
    }
    options = [
        ApplicationCommandOption('voice-0', 'voice', ApplicationCommandOptionType.string),
        ApplicationCommandOption('voice-1', 'voice', ApplicationCommandOptionType.integer),
    ]
    option_type = ApplicationCommandOptionType.sub_command_group
    
    data = {
        'description': description,
        'description_localizations': {key.value: value for key, value in description_localizations.items()},
        'name': name,
        'name_localizations': {key.value: value for key, value in name_localizations.items()},
        'options': [option.to_data(defaults = True) for option in options],
        'type': option_type.value,
    }
    
    option = ApplicationCommandOption.from_data(data)
    _assert_fields_set(option)
    
    vampytest.assert_eq(option.description, description)
    vampytest.assert_eq(option.description_localizations, description_localizations)
    vampytest.assert_eq(option.name, name)
    vampytest.assert_eq(option.name_localizations, name_localizations)
    vampytest.assert_eq(option.options, tuple(options))
    vampytest.assert_is(option.type, option_type)


def test__ApplicationCommandOption__to_data__string():
    """
    Tests whether ``ApplicationCommandOption.to_data`` works as intended.
    
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
    
    required_fields = {
        'name': name,
        'description': description,
        'type': option_type.value,
        'autocomplete': autocomplete,
        'description_localizations': {key.value: value for key, value in description_localizations.items()},
        'max_length': max_length,
        'min_length': min_length,
        'name_localizations': {key.value: value for key, value in name_localizations.items()},
        'required': required,
    }
    
    output = option.to_data(defaults = True)
    output = {key: value for key, value in output.items() if key in required_fields.keys()}
    
    vampytest.assert_eq(
        output,
        required_fields,
    )


def test__ApplicationCommandOption__to_data__channel():
    """
    Tests whether ``ApplicationCommandOption.to_data`` works as intended.
    
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
    
    required_fields = {
        'name': name,
        'description': description,
        'type': option_type.value,
        'channel_types': [channel_type.value for channel_type in channel_types],
    }
    
    output = option.to_data(defaults = True)
    output = {key: value for key, value in output.items() if key in required_fields.keys()}
    
    vampytest.assert_eq(
        output,
        required_fields,
    )


def test__ApplicationCommandOption__to_data__integer():
    """
    Tests whether ``ApplicationCommandOption.to_data`` works as intended.
    
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
    
    required_fields = {
        'name': name,
        'description': description,
        'type': option_type.value,
        'min_value': min_value,
        'max_value': max_value,
    }
    
    output = option.to_data(defaults = True)
    output = {key: value for key, value in output.items() if key in required_fields.keys()}
    
    vampytest.assert_eq(
        output,
        required_fields,
    )


def test__ApplicationCommandOption__to_data__float():
    """
    Tests whether ``ApplicationCommandOption.to_data`` works as intended.
    
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
    
    required_fields = {
        'name': name,
        'description': description,
        'type': option_type.value,
        'choices': [choice.to_data(defaults = True) for choice in choices],
    }
    
    output = option.to_data(defaults = True)
    output = {key: value for key, value in output.items() if key in required_fields.keys()}
    
    vampytest.assert_eq(
        output,
        required_fields,
    )


def test__ApplicationCommandOption__to_data__sub_command():
    """
    Tests whether ``ApplicationCommandOption.to_data`` works as intended.
    
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
    
    required_fields = {
        'name': name,
        'description': description,
        'type': option_type.value,
        'default': default,
        'options': [option.to_data(defaults = True) for option in options],
    }
    
    output = option.to_data(defaults = True)
    output = {key: value for key, value in output.items() if key in required_fields.keys()}
    
    vampytest.assert_eq(
        output,
        required_fields,
    )
