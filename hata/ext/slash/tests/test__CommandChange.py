import vampytest

from ....discord.application_command import ApplicationCommandTargetType

from ..command import CommandBaseApplicationCommand, ContextCommand
from ..slasher import CommandChange


def _assert_fields_set(command_change):
    """
    Tests whether every fields are set of the given command change.
    
    Parameters
    ----------
    command_change : ``CommandChange``
        The command change to test.
    """
    vampytest.assert_instance(command_change, CommandChange)
    vampytest.assert_instance(command_change.added, bool)
    vampytest.assert_instance(command_change.command, CommandBaseApplicationCommand)


async def command_function():
    pass


def test__CommandBaseApplicationCommand__new():
    """
    Tests whether ``CommandBaseApplicationCommand.__new__`` works as intended.
    """
    added = True
    target_type = ApplicationCommandTargetType.channel
    
    command = ContextCommand(command_function, is_global = True, target_type = target_type)
    
    command_change = CommandChange(added, command)
    _assert_fields_set(command_change)
    
    vampytest.assert_eq(command_change.added, added)
    vampytest.assert_is(command_change.command, command)


def test__CommandBaseApplicationCommand__repr():
    """
    Tests whether ``CommandBaseApplicationCommand.__repr__`` works as intended.
    """
    added = True
    target_type = ApplicationCommandTargetType.channel
    
    command = ContextCommand(command_function, is_global = True, target_type = target_type)
    
    command_change = CommandChange(added, command)
    
    output = repr(command_change)
    vampytest.assert_instance(output, str)


def test__CommandBaseApplicationCommand__unpack():
    """
    Tests whether ``CommandBaseApplicationCommand`` unpacking works as intended.
    """
    added = True
    target_type = ApplicationCommandTargetType.channel
    
    command = ContextCommand(command_function, is_global = True, target_type = target_type)
    
    command_change = CommandChange(added, command)
    
    output = (*command_change,)
    
    vampytest.assert_eq(len(output), len(command_change))
