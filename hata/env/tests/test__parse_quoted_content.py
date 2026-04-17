import vampytest

from ..parsing import (
    ERROR_CODE_QUOTE_NOT_CLOSED, PARSED_STATE_END, PARSED_STATE_FAILURE, PARSED_STATE_SUCCESS, ParserState,
    embed_error_code, parse_quoted_content
)


@vampytest.call_with(
    '', 0, '\'', (embed_error_code(PARSED_STATE_FAILURE | PARSED_STATE_END, ERROR_CODE_QUOTE_NOT_CLOSED), None), 0
)
@vampytest.call_with(
    'a', 1, '\'', (embed_error_code(PARSED_STATE_FAILURE | PARSED_STATE_END, ERROR_CODE_QUOTE_NOT_CLOSED), None), 1
)
@vampytest.call_with(
    'a', 0, '\'', (embed_error_code(PARSED_STATE_FAILURE | PARSED_STATE_END, ERROR_CODE_QUOTE_NOT_CLOSED), 'a'), 1
)
@vampytest.call_with(
    '\'a\'', 1, '\'', (PARSED_STATE_SUCCESS, 'a'), 3
)
@vampytest.call_with(
    '\'aa\'a', 1, '\'', (PARSED_STATE_SUCCESS, 'aa'), 4
)
@vampytest.call_with(
    '\'a\\\'\'', 1, '\'', (PARSED_STATE_SUCCESS, 'a\''), 5
)
@vampytest.call_with(
    '\'a\\q\'', 1, '\'', (PARSED_STATE_SUCCESS, 'a\\q'), 5
)
@vampytest.call_with(
    '\"a\"', 1, '"', (PARSED_STATE_SUCCESS, 'a'), 3
)
def test__parse_quoted_content(value, position, expected_ending, expected_output, expected_position):
    """
    Tests whether ``parse_quoted_content`` works as intended.
    
    Parameters
    ----------
    value : `str`
        Value to parse.
    position : `int`
        The position to start parsing at.
    expected_ending : `str`
        Expected ending character to parse till. (Input too.)
    expected_output : `tuple` (`int`, `None` | `str`)
        The expected output to be returned.
    expected_position : `int`
        The expected position of the parser after parsing the content.
    """
    state = ParserState(value)
    state.position = position
    
    output = parse_quoted_content(state, expected_ending)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(state.position, expected_position)
