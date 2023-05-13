import vampytest

from ..parsing import PARSED_STATE_END, PARSED_STATE_FAILURE, PARSED_STATE_SUCCESS, ParserState, parse_string_content


@vampytest.call_with('', 0, '\'', (PARSED_STATE_FAILURE | PARSED_STATE_END, None), 0)
@vampytest.call_with('a', 1, '\'', (PARSED_STATE_FAILURE | PARSED_STATE_END, None), 1)
@vampytest.call_with('a', 0, '\'', (PARSED_STATE_FAILURE | PARSED_STATE_END, 'a'), 1)
@vampytest.call_with('\'a\'', 1, '\'', (PARSED_STATE_SUCCESS, 'a'), 3)
@vampytest.call_with('\'aa\'a', 1, '\'', (PARSED_STATE_SUCCESS, 'aa'), 4)
@vampytest.call_with('\'a\\\'\'', 1, '\'', (PARSED_STATE_SUCCESS, 'a\''), 5)
@vampytest.call_with('\'a\\q\'', 1, '\'', (PARSED_STATE_SUCCESS, 'a\\q'), 5)
@vampytest.call_with('\"a\"', 1, '"', (PARSED_STATE_SUCCESS, 'a'), 3)
def test__parse_string_content(value, position, expected_ending, expected_output, expected_position):
    """
    Tests whether ``parse_string_content`` works as intended.
    """
    state = ParserState(value)
    state.position = position
    
    output = parse_string_content(state, expected_ending)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(state.position, expected_position)
