import vampytest

from ..parsing import PARSED_STATE_END, PARSED_STATE_SUCCESS, ParserState, parse_next


@vampytest.call_with('', 0, (PARSED_STATE_END, None), 0)
@vampytest.call_with('a', 1, (PARSED_STATE_END, None), 1)
@vampytest.call_with('a_12', 0, (PARSED_STATE_SUCCESS, 'a'), 1)
@vampytest.call_with('\n', 0, (PARSED_STATE_SUCCESS, '\n'), 1)
def test__parse_next(value, position, expected_output, expected_position):
    """
    Tests whether ``parse_next`` works as intended.
    """
    state = ParserState(value)
    state.position = position
    
    output = parse_next(state)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(state.position, expected_position)
