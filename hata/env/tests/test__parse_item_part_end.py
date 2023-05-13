import vampytest

from ..parsing import PARSED_STATE_END, PARSED_STATE_SUCCESS, ParserState, parse_item_part_end


@vampytest.call_with('', 0, None, None, (PARSED_STATE_END | PARSED_STATE_SUCCESS, None), 0)
@vampytest.call_with('', 0, 'a', 'b', (PARSED_STATE_END | PARSED_STATE_SUCCESS, ('a', 'b')), 0)
@vampytest.call_with('  ', 0, None, None, (PARSED_STATE_SUCCESS | PARSED_STATE_END, None), 2)
@vampytest.call_with('  ', 0, 'a', 'b', (PARSED_STATE_SUCCESS | PARSED_STATE_END, ('a', 'b')), 2)
@vampytest.call_with(' \n', 0, None, None, (PARSED_STATE_SUCCESS, None), 2)
@vampytest.call_with(' \n', 0, 'a', 'b', (PARSED_STATE_SUCCESS, ('a', 'b')), 2)
@vampytest.call_with(' #', 0, None, None, (PARSED_STATE_END | PARSED_STATE_SUCCESS, None), 2)
@vampytest.call_with(' #', 0, 'a', 'b', (PARSED_STATE_END | PARSED_STATE_SUCCESS, ('a', 'b')), 2)
@vampytest.call_with(' #a\na', 0, None, None, (PARSED_STATE_SUCCESS, None), 4)
@vampytest.call_with(' #a\na', 0, 'a', 'b', (PARSED_STATE_SUCCESS, ('a', 'b')), 4)
@vampytest.call_with('a', 0, None, None, None, 0)
@vampytest.call_with(' a', 0, None, None, None, 1)
def test__parse_item_part_end(value, position, parsed_key, parsed_value, expected_output, expected_position):
    """
    Tests whether ``parse_item_part_end`` works as intended.
    """
    state = ParserState(value)
    state.position = position
    
    output = parse_item_part_end(state, parsed_key, parsed_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(state.position, expected_position)
