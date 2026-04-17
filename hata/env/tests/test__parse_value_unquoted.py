import vampytest

from ..parsing import PARSED_STATE_END, PARSED_STATE_FAILURE, PARSED_STATE_SUCCESS, ParserState, parse_value_unquoted


@vampytest.call_with('', 0, (PARSED_STATE_END, None), 0)
@vampytest.call_with('a', 1, (PARSED_STATE_END, None), 1)
@vampytest.call_with('a_12', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, 'a_12'), 4)
@vampytest.call_with('_', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, '_'), 1)
@vampytest.call_with('a_12 ', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, 'a_12'), 5)
@vampytest.call_with('12_a', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, '12_a'), 4)
@vampytest.call_with('#', 0, (PARSED_STATE_FAILURE, None), 0)
@vampytest.call_with('a #', 0, (PARSED_STATE_SUCCESS, 'a'), 2)
@vampytest.call_with('a \n', 0, (PARSED_STATE_SUCCESS, 'a'), 2)
def test__parse_value_unquoted(value, position, expected_output, expected_position):
    """
    Tests whether ``parse_value_unquoted`` works as intended.
    """
    state = ParserState(value)
    state.position = position
    
    output = parse_value_unquoted(state)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(state.position, expected_position)
