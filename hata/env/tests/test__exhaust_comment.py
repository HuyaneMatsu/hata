import vampytest

from ..parsing import PARSED_STATE_END, PARSED_STATE_FAILURE, PARSED_STATE_SUCCESS, ParserState, exhaust_comment


@vampytest.call_with('', 0, PARSED_STATE_END, 0)
@vampytest.call_with('a', 1, PARSED_STATE_END, 1)
@vampytest.call_with('a', 0, PARSED_STATE_FAILURE, 0)
@vampytest.call_with('\n', 0, PARSED_STATE_FAILURE, 0)
@vampytest.call_with('#', 0, PARSED_STATE_SUCCESS | PARSED_STATE_END, 1)
@vampytest.call_with('#\n', 0, PARSED_STATE_SUCCESS, 2)
@vampytest.call_with('#\n\n', 0, PARSED_STATE_SUCCESS, 2)
@vampytest.call_with('#aa', 0, PARSED_STATE_SUCCESS | PARSED_STATE_END, 3)
@vampytest.call_with('#aa\n\n', 0, PARSED_STATE_SUCCESS, 4)
def test__exhaust_comment(value, position, expected_output, expected_position):
    """
    Tests whether ``exhaust_comment`` works as intended.
    """
    state = ParserState(value)
    state.position = position
    
    output = exhaust_comment(state)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(state.position, expected_position)
