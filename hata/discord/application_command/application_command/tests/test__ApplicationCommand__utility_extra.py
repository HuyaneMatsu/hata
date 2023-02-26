import vampytest

from ....localization import Locale
from ....permission import Permission
from ....guild import Guild
from ....utils import id_to_datetime

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..application_command import ApplicationCommand
from ..preinstanced import ApplicationCommandTargetType

from .test__ApplicationCommand__constructor import _assert_fields_set


def test__ApplicationCommand__mention_sub_command():
    """
    Tests whether ``ApplicationCommand.mention_sub_command`` works as intended.
    """
    name = 'kimi'
    sub_command_names = ['no', 'kiseki']
    
    application_command = ApplicationCommand(name)
    
    output = application_command.mention_sub_command(*sub_command_names)
    
    vampytest.assert_instance(output, str)
    
    for sub_command_name in sub_command_names:
        vampytest.assert_in(sub_command_name, output)


def test__ApplicationCommand__mention_with():
    """
    Tests whether ``ApplicationCommand.mention_sub_command`` works as intended.
    """
    name = 'kimi'
    with_ = 'no kiseki'
    
    application_command = ApplicationCommand(name)
    
    output = application_command.mention_with(with_)
    
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in(with_, output)


def test__ApplicationCommand__mention():
    """
    Tests whether ``ApplicationCommand.mention`` works as intended.
    """
    name = 'kimi'
    
    application_command = ApplicationCommand(name)
    
    output = application_command.mention
    
    vampytest.assert_instance(output, str)


def test__ApplicationCommand__display_name():
    """
    Tests whether ``ApplicationCommand.display_name`` works as intended.
    """
    name = 'kimi'
    
    application_command = ApplicationCommand(name)
    
    output = application_command.display_name
    
    vampytest.assert_instance(output, str)
    vampytest.assert_in(name.casefold(), output.casefold())


def test__ApplicationCommand__edited_at():
    """
    Tests whether ``ApplicationCommand.edited_at`` works as intended.
    """
    version = 202302260014
    
    for input_value, expected_output in (
        (0, None),
        (version, id_to_datetime(version)),
    ):
        application_command = ApplicationCommand('kimi')
        application_command.version = input_value
        
        vampytest.assert_eq(application_command.edited_at, expected_output)


def test__ApplicationCommand__partial():
    """
    Tests whether ``ApplicationCommand.partial`` works as intended.
    """
    application_command_id = 202302260015
    
    for input_value, expected_output in (
        (0, True),
        (application_command_id, False),
    ):
        application_command = ApplicationCommand('kimi')
        application_command.id = input_value
        
        vampytest.assert_eq(application_command.partial, expected_output)


def test__ApplicationCommand__is_context_command():
    """
    Tests whether ``ApplicationCommand.is_context_command`` works as intended.
    """
    for input_value, expected_output in (
        (ApplicationCommandTargetType.message, True),
        (ApplicationCommandTargetType.chat, False),
    ):
        application_command = ApplicationCommand('kimi', target_type = input_value)
        
        vampytest.assert_eq(application_command.is_context_command(), expected_output)


def test__ApplicationCommand__is_slash_command():
    """
    Tests whether ``ApplicationCommand.is_slash_command`` works as intended.
    """
    for input_value, expected_output in (
        (ApplicationCommandTargetType.message, False),
        (ApplicationCommandTargetType.chat, True),
    ):
        application_command = ApplicationCommand('kimi', target_type = input_value)
        
        vampytest.assert_eq(application_command.is_slash_command(), expected_output)


def test__ApplicationCommand__guild():
    """
    Tests whether ``ApplicationCommand.guild`` works as intended.
    """
    guild_id_0 = 202302260016
    guild_id_1 = 202302260017
    
    for input_value, expected_output in (
        (0, None),
        (guild_id_0, None),
        (guild_id_1, Guild.precreate(guild_id_1)),
    ):
        application_command = ApplicationCommand('kimi')
        application_command.guild_id = input_value
        
        vampytest.assert_eq(application_command.guild, expected_output)


def test__ApplicationCommand__iter_options():
    """
    Tests whether ``ApplicationCommand.iter_options`` works as intended.
    """
    option_0 = ApplicationCommandOption('okuu', 'orin', ApplicationCommandOptionType.string)
    option_1 = ApplicationCommandOption('orin', 'okuu', ApplicationCommandOptionType.integer)
    
    for input_value, expected_output in (
        (None, []),
        ([option_0], [option_0]),
        ([option_0, option_1], [option_0, option_1]),
    ):
        option = ApplicationCommand('kimi', options = input_value)
        vampytest.assert_eq([*option.iter_options()], expected_output)
