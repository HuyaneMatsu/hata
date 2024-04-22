from os import terminal_size as TerminalSize

import vampytest

from ..payload_renderer import LINE_WIDTH_DEFAULT, _get_terminal_line_width


def test__get_terminal_line_width__os_error():
    """
    Tests whether ``_get_terminal_line_width`` works as intended.
    
    Case: `OSError`.
    """
    def get_terminal_size_mock():
        raise OSError()
    
    mocked = vampytest.mock_globals(
        _get_terminal_line_width,
        get_terminal_size = get_terminal_size_mock,
    )
    
    output = mocked()
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, LINE_WIDTH_DEFAULT)


def test__get_terminal_line_width__return():
    """
    Tests whether ``_get_terminal_line_width`` works as intended.
    
    Case: Return.
    """
    terminal_width = 20
    
    def get_terminal_size_mock():
        nonlocal terminal_width
        return TerminalSize((terminal_width, 0))
    
    mocked = vampytest.mock_globals(
        _get_terminal_line_width,
        get_terminal_size = get_terminal_size_mock,
    )
    
    output = mocked()
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, terminal_width)
