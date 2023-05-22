import vampytest

from ..parsing import (
    ERROR_CODE_KEY_STARTER_INVALID, PARSED_STATE_END, PARSED_STATE_FAILURE, PARSED_STATE_SUCCESS, ParserState,
    embed_error_code, parse_key_unquoted
)


@vampytest.call_with('', 0, (PARSED_STATE_END, None), 0)
@vampytest.call_with('a', 1, (PARSED_STATE_END, None), 1)
@vampytest.call_with('a_12', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, 'a_12'), 4)
@vampytest.call_with('_', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, '_'), 1)
@vampytest.call_with('a_12 ', 0, (PARSED_STATE_SUCCESS, 'a_12'), 4)
@vampytest.call_with('12_a', 0, (embed_error_code(PARSED_STATE_FAILURE, ERROR_CODE_KEY_STARTER_INVALID), None), 0)
@vampytest.call_with('#', 0, (embed_error_code(PARSED_STATE_FAILURE, ERROR_CODE_KEY_STARTER_INVALID), None), 0)
def test__parse_key_unquoted(value, position, expected_output, expected_position):
    """
    Tests whether ``parse_key_unquoted`` works as intended.
    
    Parameters
    ----------
    value : `str`
        Value to parse.
    position : `int`
        Position index to start at.
    expected_output : `tuple` (`int`, `None` | `str`)
        Expected output to be returned.
    expected_position : `int`
        The expected position of the parser after parsing the key.
    """
    state = ParserState(value)
    state.position = position
    
    output = parse_key_unquoted(state)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(state.position, expected_position)
