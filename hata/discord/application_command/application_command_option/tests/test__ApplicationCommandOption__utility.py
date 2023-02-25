import vampytest

from ....channel import ChannelType
from ....localization import Locale

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..application_command_option import ApplicationCommandOption
from ..preinstanced import ApplicationCommandOptionType

from .test__ApplicationCommandOption__constructor import _assert_fields_set


def test__ApplicationCommandOption__copy__string():
    """
    Tests whether ``ApplicationCommandOption.copy`` works as intended.
    
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
    copy = option.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy, option)


def test__ApplicationCommandOption__copy__channel():
    """
    Tests whether ``ApplicationCommandOption.copy`` works as intended.
    
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
    copy = option.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy, option)


def test__ApplicationCommandOption__copy__integer():
    """
    Tests whether ``ApplicationCommandOption.copy`` works as intended.
    
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
    copy = option.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy, option)


def test__ApplicationCommandOption__copy__float():
    """
    Tests whether ``ApplicationCommandOption.copy`` works as intended.
    
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
    copy = option.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy, option)


def test__ApplicationCommandOption__copy__sub_command():
    """
    Tests whether ``ApplicationCommandOption.copy`` works as intended.
    
    Case: No fields given | sub-command.
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
    copy = option.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy, option)


def test__ApplicationCommandOption__copy_with__0__string():
    """
    Tests whether ``ApplicationCommandOption.copy_with`` works as intended.
    
    Case: No fields given | string.
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
    copy = option.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy, option)


def test__ApplicationCommandOption__copy_with__0__channel():
    """
    Tests whether ``ApplicationCommandOption.copy_with`` works as intended.
    
    Case: No fields given | channel.
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
    copy = option.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy, option)


def test__ApplicationCommandOption__copy_with__0__integer():
    """
    Tests whether ``ApplicationCommandOption.copy_with`` works as intended.
    
    Case: No fields given | integer.
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
    copy = option.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy, option)


def test__ApplicationCommandOption__copy_with__0__float():
    """
    Tests whether ``ApplicationCommandOption.copy_with`` works as intended.
    
    Case: No fields given | float.
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
    copy = option.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy, option)


def test__ApplicationCommandOption__copy_with__0__sub_command():
    """
    Tests whether ``ApplicationCommandOption.copy_with`` works as intended.
    
    Case: No fields given | sub-command.
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
    copy = option.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy, option)


def test__ApplicationCommandOption__copy_with__1__string():
    """
    Tests whether ``ApplicationCommandOption.copy_with`` works as intended.
    
    Case: All fields given | string.
    """
    old_name = 'primrose'
    old_description = 'flower'
    old_option_type = ApplicationCommandOptionType.string
    old_autocomplete = True
    old_description_localizations = {
        Locale.german: 'hartmann',
    }
    old_max_length = 30
    old_min_length = 10
    old_name_localizations = {
        Locale.german: 'satori',
    }
    old_required = True
    
    new_name = 'momiji'
    new_description = 'yukari'
    new_option_type = ApplicationCommandOptionType.string
    new_autocomplete = False
    new_description_localizations = {
        Locale.german: 'ran',
    }
    new_max_length = 6
    new_min_length = 4
    new_name_localizations = {
        Locale.german: 'chen',
    }
    new_required = False
    
    option = ApplicationCommandOption(
        old_name,
        old_description,
        old_option_type,
        autocomplete = old_autocomplete,
        description_localizations = old_description_localizations,
        max_length = old_max_length,
        min_length = old_min_length,
        name_localizations = old_name_localizations,
        required = old_required,
    )
    copy = option.copy_with(
        name = new_name,
        description = new_description,
        option_type = new_option_type,
        autocomplete = new_autocomplete,
        description_localizations = new_description_localizations,
        max_length = new_max_length,
        min_length = new_min_length,
        name_localizations = new_name_localizations,
        required = new_required,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_is(copy.type, new_option_type)
    vampytest.assert_eq(copy.autocomplete, new_autocomplete)
    vampytest.assert_eq(copy.description_localizations, new_description_localizations)
    vampytest.assert_eq(copy.max_length, new_max_length)
    vampytest.assert_eq(copy.min_length, new_min_length)
    vampytest.assert_eq(copy.name_localizations, new_name_localizations)
    vampytest.assert_eq(copy.required, new_required)


def test__ApplicationCommandOption__copy_with__1__channel():
    """
    Tests whether ``ApplicationCommandOption.copy_with`` works as intended.
    
    Case: All fields given | channel.
    """
    old_name = 'primrose'
    old_description = 'flower'
    old_option_type = ApplicationCommandOptionType.channel
    old_channel_types = [ChannelType.private, ChannelType.guild_forum]
    
    new_name = 'primrose'
    new_description = 'flower'
    new_option_type = ApplicationCommandOptionType.channel
    new_channel_types = [ChannelType.private_group]
    
    option = ApplicationCommandOption(
        old_name,
        old_description,
        old_option_type,
        channel_types = old_channel_types,
    )
    copy = option.copy_with(
        name = new_name,
        description = new_description,
        option_type = new_option_type,
        channel_types = new_channel_types,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_is(copy.type, new_option_type)
    vampytest.assert_eq(copy.channel_types, tuple(new_channel_types))


def test__ApplicationCommandOption__copy_with__1__integer():
    """
    Tests whether ``ApplicationCommandOption.copy_with`` works as intended.
    
    Case: All fields given | integer.
    """
    old_name = 'primrose'
    old_description = 'flower'
    old_option_type = ApplicationCommandOptionType.integer
    old_min_value = -10
    old_max_value = +10
    
    new_name = 'momiji'
    new_description = 'yukari'
    new_option_type = ApplicationCommandOptionType.integer
    new_min_value = -9
    new_max_value = +9
    
    option = ApplicationCommandOption(
        old_name,
        old_description,
        old_option_type,
        min_value = old_min_value,
        max_value = old_max_value,
    )
    copy = option.copy_with(
        name = new_name,
        description = new_description,
        option_type = new_option_type,
        min_value = new_min_value,
        max_value = new_max_value,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_is(copy.type, new_option_type)
    vampytest.assert_eq(copy.min_value, new_min_value)
    vampytest.assert_eq(copy.max_value, new_max_value)


def test__ApplicationCommandOption__copy_with__1__float():
    """
    Tests whether ``ApplicationCommandOption.copy_with`` works as intended.
    
    Case: All fields given | float.
    """
    old_name = 'primrose'
    old_description = 'flower'
    old_option_type = ApplicationCommandOptionType.float
    old_choices = [
        ApplicationCommandOptionChoice('voice', 1.2),
        ApplicationCommandOptionChoice('voice', 2.4),
    ]
    
    new_name = 'momiji'
    new_description = 'yukari'
    new_option_type = ApplicationCommandOptionType.float
    new_choices = [
        ApplicationCommandOptionChoice('momiji', 1.2),
        ApplicationCommandOptionChoice('aya', 2.4),
    ]
    
    option = ApplicationCommandOption(
        old_name,
        old_description,
        old_option_type,
        choices = old_choices,
    )
    copy = option.copy_with(
        name = new_name,
        description = new_description,
        option_type = new_option_type,
        choices = new_choices,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_is(copy.type, new_option_type)
    vampytest.assert_eq(copy.choices, tuple(new_choices))



def test__ApplicationCommandOption__copy_with__1__sub_command():
    """
    Tests whether ``ApplicationCommandOption.copy_with`` works as intended.
    
    Case: All fields given | sub-command.
    """
    old_name = 'primrose'
    old_description = 'flower'
    old_option_type = ApplicationCommandOptionType.sub_command
    old_default = True
    old_options = [
        ApplicationCommandOption('voice-0', 'voice', ApplicationCommandOptionType.string),
        ApplicationCommandOption('voice-1', 'voice', ApplicationCommandOptionType.integer),
    ]
    
    new_name = 'momiji'
    new_description = 'yukari'
    new_option_type = ApplicationCommandOptionType.sub_command
    new_default = True
    new_options = [
        ApplicationCommandOption('voice-0', 'aya', ApplicationCommandOptionType.string),
        ApplicationCommandOption('voice-1', 'aya', ApplicationCommandOptionType.integer),
    ]
    
    option = ApplicationCommandOption(
        old_name,
        old_description,
        old_option_type,
        default = old_default,
        options = old_options,
    )
    copy = option.copy_with(
        name = new_name,
        description = new_description,
        option_type = new_option_type,
        default = new_default,
        options = new_options,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, option)
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_is(copy.type, new_option_type)
    vampytest.assert_eq(copy.default, new_default)
    vampytest.assert_eq(copy.options, tuple(new_options))


def test__ApplicationCommandOption__iter_choices():
    """
    Tests whether ``ApplicationCommandOption.iter_choices`` works as intended.
    """
    choice_0 = ApplicationCommandOptionChoice('aya')
    choice_1 = ApplicationCommandOptionChoice('momiji')
    
    for input_value, expected_output in (
        (None, []),
        ([choice_0], [choice_0]),
        ([choice_0, choice_1], [choice_0, choice_1]),
    ):
        option = ApplicationCommandOption('ibuki', 'suika', ApplicationCommandOptionType.string, choices = input_value)
        vampytest.assert_eq([*option.iter_choices()], expected_output)


def test__ApplicationCommandOption__iter_options():
    """
    Tests whether ``ApplicationCommandOption.iter_options`` works as intended.
    """
    option_0 = ApplicationCommandOption('voice-0', 'aya', ApplicationCommandOptionType.string)
    option_1 = ApplicationCommandOption('voice-1', 'aya', ApplicationCommandOptionType.integer)
    
    for input_value, expected_output in (
        (None, []),
        ([option_0], [option_0]),
        ([option_0, option_1], [option_0, option_1]),
    ):
        option = ApplicationCommandOption('ibuki', 'suika', ApplicationCommandOptionType.string, options = input_value)
        vampytest.assert_eq([*option.iter_options()], expected_output)


def test__ApplicationCommandOption__with_translation():
    """
    Tests whether ``ApplicationCommandOption.with_translation` works as intended.
    """
    option = ApplicationCommandOption(
        'yukari',
        'ran',
        ApplicationCommandOptionType.string,
        choices = [ApplicationCommandOptionChoice('chen', 'chen',)],
        options = [ApplicationCommandOption('aya', 'aya', ApplicationCommandOptionType.string)],
    )
    
    translation_table = {
        Locale.german: {
            'yukari': 'satori',
            'ran': 'orin',
            'chen': 'okuu',
            'aya': 'momiji',
        }
    }
    
    expected_output = ApplicationCommandOption(
        'yukari',
        'ran',
        ApplicationCommandOptionType.string,
        name_localizations = {
            Locale.german: 'satori',
        },
        description_localizations = {
            Locale.german: 'orin',
        },
        choices = [
            ApplicationCommandOptionChoice(
                'chen',
                'chen',
                name_localizations = {
                    Locale.german: 'okuu',
                }
            )
        ],
        options = [
            ApplicationCommandOption(
                'aya',
                'aya',
                ApplicationCommandOptionType.string,
                name_localizations = {
                    Locale.german: 'momiji',
                },
                description_localizations = {
                    Locale.german: 'momiji',
                },
            ),
        ],
    )
    
    output = option.with_translation(translation_table)
    vampytest.assert_eq(output, expected_output)
