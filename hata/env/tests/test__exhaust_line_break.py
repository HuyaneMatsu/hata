import vampytest

from ..parsing import PARSED_STATE_END, PARSED_STATE_FAILURE, PARSED_STATE_SUCCESS, ParserState, exhaust_line_break


@vampytest.call_with('', 0, PARSED_STATE_END, 0)
@vampytest.call_with('a', 0, PARSED_STATE_FAILURE, 0)
@vampytest.call_with('a', 1, PARSED_STATE_END, 1)
@vampytest.call_with('\r', 1, PARSED_STATE_END, 1)
@vampytest.call_with('\n', 1, PARSED_STATE_END, 1)
@vampytest.call_with('\r', 0, PARSED_STATE_SUCCESS | PARSED_STATE_END, 1)
@vampytest.call_with('\r\n', 0, PARSED_STATE_SUCCESS, 2)
@vampytest.call_with('\n', 0, PARSED_STATE_SUCCESS, 1)
@vampytest.call_with('a\n', 1, PARSED_STATE_SUCCESS, 2)
def test__exhaust_line_break(value, position, expected_output, expected_position):
    """
    Tests whether ``exhaust_line_break`` works as intended.
    
    Parameters
    ----------
    value : `str`
        The value to parse.
    position : `int`
        Start position to parse from.
    expected_output : `int`
        Bitwise flag of the outcome of the operation.
    expected_position : `int`
        The expected position after parsing.
    """
    state = ParserState(value)
    state.position = position
    
    output = exhaust_line_break(state)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(state.position, expected_position)
    
    if position != expected_position:
        vampytest.assert_eq(state.line_index, 1)
        vampytest.assert_eq(state.line_start, expected_position)
