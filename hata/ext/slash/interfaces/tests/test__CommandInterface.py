import vampytest

from ..autocomplete import CommandInterface


def test__CommandInterface__get_command_function():
    """
    Tests whether ``CommandInterface.get_command_function`` works as intended.
    """
    output = CommandInterface().get_command_function()
    vampytest.assert_is(output, None)
