import vampytest

from ..parsing import (
    ERROR_CODE_KEY_STARTER_INVALID, ERROR_CODE_QUOTE_NOT_CLOSED, PARSED_STATE_END, PARSED_STATE_FAILURE,
    PARSED_STATE_SUCCESS, ParserState, embed_error_code, parse_key_or_value
)


@vampytest.call_with(
    '', 0, True, (PARSED_STATE_FAILURE | PARSED_STATE_END, None), 0
)
@vampytest.call_with(
    ' ', 0, True, (embed_error_code(PARSED_STATE_FAILURE, ERROR_CODE_KEY_STARTER_INVALID), None), 0
)
@vampytest.call_with(
    ' ', 0, False, (PARSED_STATE_SUCCESS | PARSED_STATE_END, None), 1
)
@vampytest.call_with(
    ' #', 0, False, (PARSED_STATE_SUCCESS, None), 1
)
@vampytest.call_with(
    'a', 0, True, (PARSED_STATE_SUCCESS | PARSED_STATE_END, 'a'), 1
)
@vampytest.call_with(
    ' a', 1, True, (PARSED_STATE_SUCCESS | PARSED_STATE_END, 'a'), 2
)
@vampytest.call_with(
    'a', 0, False, (PARSED_STATE_SUCCESS | PARSED_STATE_END, 'a'), 1
)
@vampytest.call_with(
    'a #', 0, True, (PARSED_STATE_SUCCESS, 'a'), 1
)
@vampytest.call_with(
    'a #', 0, False, (PARSED_STATE_SUCCESS, 'a'), 2
)
@vampytest.call_with(
    'aa\n', 0, True, (PARSED_STATE_SUCCESS, 'aa'), 2
)
@vampytest.call_with(
    'aa\n', 0, False, (PARSED_STATE_SUCCESS, 'aa'), 2
)
@vampytest.call_with(
    '1', 0, True, (embed_error_code(PARSED_STATE_FAILURE, ERROR_CODE_KEY_STARTER_INVALID), None), 0
)
@vampytest.call_with(
    '1', 0, False, (PARSED_STATE_SUCCESS | PARSED_STATE_END, '1'), 1
)
@vampytest.call_with(
    '\'aa\'', 0, True, (PARSED_STATE_SUCCESS, 'aa'), 4
)
@vampytest.call_with(
    '\"aa\"', 0, False, (PARSED_STATE_SUCCESS, 'aa'), 4
)
@vampytest.call_with(
    '\"aa', 0, False, (embed_error_code(PARSED_STATE_FAILURE | PARSED_STATE_END, ERROR_CODE_QUOTE_NOT_CLOSED), 'aa'), 3
)
def test__parse_key_or_value(value, position, is_key, expected_output, expected_position):
    """
    Tests whether ``parse_key_or_value`` works as intended.
    
    Parameters
    ----------
    value : `str`
        Value to parse.
    position : `int`
        The position to start parsing at.
    is_key : `bool`
        Whether we are parsing a key or a value. (Input too.)
    expected_output : `tuple` (`int`, `None` | `str`)
        The expected output to be returned.
    expected_position : `int`
        The expected position of the parser after parsing the key or value.
    """
    state = ParserState(value)
    state.position = position
    
    output = parse_key_or_value(state, is_key)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(state.position, expected_position)
