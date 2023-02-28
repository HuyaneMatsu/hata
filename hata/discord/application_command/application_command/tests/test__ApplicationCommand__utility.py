import vampytest

from ....localization import Locale
from ....permission import Permission

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..application_command import ApplicationCommand
from ..preinstanced import ApplicationCommandTargetType

from .test__ApplicationCommand__constructor import _assert_fields_set


def test__ApplicationCommand__copy():
    """
    Tests whether ``ApplicationCommand.copy`` works as intended.
    """
    name = 'owo'
    description = 'description'
    allow_in_dm = True
    description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    name_localizations = {
        Locale.thai: 'nay',
        Locale.czech: 'lay',
    }
    nsfw = True
    options = [
        ApplicationCommandOption(
            'option',
            'optional',
            ApplicationCommandOptionType.string,

        )
    ]
    required_permissions = Permission().update_by_keys(administrator = True)
    target_type = ApplicationCommandTargetType.chat
    
    application_command = ApplicationCommand(
        name,
        description,
        allow_in_dm = allow_in_dm,
        description_localizations = description_localizations,
        name_localizations = name_localizations,
        nsfw = nsfw,
        options = options,
        required_permissions = required_permissions,
        target_type = target_type,
    )
    
    copy = application_command.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(application_command, copy)
    vampytest.assert_eq(application_command, copy)


def test__ApplicationCommand__copy_with__0():
    """
    Tests whether ``ApplicationCommand.copy_with`` works as intended.
    
    Case: No fields given.
    """
    name = 'owo'
    description = 'description'
    allow_in_dm = True
    description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    name_localizations = {
        Locale.thai: 'nay',
        Locale.czech: 'lay',
    }
    nsfw = True
    options = [
        ApplicationCommandOption(
            'option',
            'optional',
            ApplicationCommandOptionType.string,

        )
    ]
    required_permissions = Permission().update_by_keys(administrator = True)
    target_type = ApplicationCommandTargetType.chat
    
    application_command = ApplicationCommand(
        name,
        description,
        allow_in_dm = allow_in_dm,
        description_localizations = description_localizations,
        name_localizations = name_localizations,
        nsfw = nsfw,
        options = options,
        required_permissions = required_permissions,
        target_type = target_type,
    )
    
    copy = application_command.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(application_command, copy)
    vampytest.assert_eq(application_command, copy)


def test__ApplicationCommand__copy_with__1():
    """
    Tests whether ``ApplicationCommand.copy_with`` works as intended.
    
    Case: No fields given.
    """
    old_name = 'owo'
    old_description = 'description'
    old_allow_in_dm = True
    old_description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    old_name_localizations = {
        Locale.thai: 'nay',
        Locale.czech: 'lay',
    }
    old_nsfw = True
    old_options = [
        ApplicationCommandOption(
            'option',
            'optional',
            ApplicationCommandOptionType.string,

        )
    ]
    old_required_permissions = Permission().update_by_keys(administrator = True)
    old_target_type = ApplicationCommandTargetType.chat
    
    new_name = 'aya'
    new_description = 'keine'
    new_allow_in_dm = True
    new_description_localizations = {
        Locale.thai: 'suika',
        Locale.czech: 'yuugi',
    }
    new_name_localizations = {
        Locale.thai: 'ibuki',
        Locale.czech: 'komeiji',
    }
    new_nsfw = True
    new_options = [
        ApplicationCommandOption(
            'koishi',
            'satori',
            ApplicationCommandOptionType.string,

        )
    ]
    new_required_permissions = Permission().update_by_keys(kick_users = True)
    new_target_type = ApplicationCommandTargetType.chat # we wont edit this or else we would drop a few other fields.
    
    application_command = ApplicationCommand(
        old_name,
        old_description,
        allow_in_dm = old_allow_in_dm,
        description_localizations = old_description_localizations,
        name_localizations = old_name_localizations,
        nsfw = old_nsfw,
        options = old_options,
        required_permissions = old_required_permissions,
        target_type = old_target_type,
    )
    
    copy = application_command.copy_with(
        name = new_name,
        description = new_description,
        allow_in_dm = new_allow_in_dm,
        description_localizations = new_description_localizations,
        name_localizations = new_name_localizations,
        nsfw = new_nsfw,
        options = new_options,
        required_permissions = new_required_permissions,
        target_type = new_target_type,
    )
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.allow_in_dm, new_allow_in_dm)
    vampytest.assert_eq(copy.description_localizations, new_description_localizations)
    vampytest.assert_eq(copy.name_localizations, new_name_localizations)
    vampytest.assert_eq(copy.nsfw, new_nsfw)
    vampytest.assert_eq(copy.options, tuple(new_options))
    vampytest.assert_eq(copy.required_permissions, new_required_permissions)
    vampytest.assert_is(copy.target_type, new_target_type)


def test__ApplicationCommand__with_translation():
    """
    Tests whether ``ApplicationCommand.with_translation` works as intended.
    """
    option = ApplicationCommand(
        'yukari',
        'ran',
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
    
    expected_output = ApplicationCommand(
        'yukari',
        'ran',
        name_localizations = {
            Locale.german: 'satori',
        },
        description_localizations = {
            Locale.german: 'orin',
        },
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
