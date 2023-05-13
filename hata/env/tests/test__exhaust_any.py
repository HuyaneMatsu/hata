import vampytest

from ..parsing import PARSED_STATE_END, PARSED_STATE_SUCCESS, ParserState, exhaust_any


@vampytest.call_with('', 0, PARSED_STATE_END, 0)
@vampytest.call_with(' ', 0, PARSED_STATE_SUCCESS, 1)
@vampytest.call_with(' ', 1, PARSED_STATE_END, 1)
def test__exhaust_any(value, position, expected_output, expected_position):
    """
    Tests whether ``exhaust_any`` works as intended.
    """
    state = ParserState(value)
    state.position = position
    
    output = exhaust_any(state)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(state.position, expected_position)
