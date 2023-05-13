import vampytest

from ..parsing import PARSED_STATE_END, PARSED_STATE_SUCCESS, ParserState, exhaust_till_comment_or_line_break


@vampytest.call_with('', 0, PARSED_STATE_END, 0)
@vampytest.call_with('a', 1, PARSED_STATE_END, 1)
@vampytest.call_with('a', 0, PARSED_STATE_SUCCESS | PARSED_STATE_END, 1)
@vampytest.call_with('aa', 0, PARSED_STATE_SUCCESS | PARSED_STATE_END, 2)
@vampytest.call_with('aa#', 0, PARSED_STATE_SUCCESS, 2)
@vampytest.call_with('aa\n', 0, PARSED_STATE_SUCCESS, 2)
@vampytest.call_with('aa\r', 0, PARSED_STATE_SUCCESS, 2)
def test__exhaust_till_comment_or_line_break(value, position, expected_output, expected_position):
    """
    Tests whether ``exhaust_till_comment_or_line_break`` works as intended.
    """
    state = ParserState(value)
    state.position = position
    
    output = exhaust_till_comment_or_line_break(state)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(state.position, expected_position)
