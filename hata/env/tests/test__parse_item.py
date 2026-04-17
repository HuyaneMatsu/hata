import vampytest

from ..parsing import (
    ERROR_CODE_EXPECTED_EQUAL_SIGN, ERROR_CODE_KEY_STARTER_INVALID, ERROR_CODE_VALUE_ALREADY_PARSED, PARSED_STATE_END,
    PARSED_STATE_FAILURE, PARSED_STATE_SUCCESS, ParserState, embed_error_code, parse_item
)


@vampytest.call_with(
    '', 0, (PARSED_STATE_END | PARSED_STATE_SUCCESS, None), 0
)
@vampytest.call_with(
    '\n', 0, (PARSED_STATE_END | PARSED_STATE_SUCCESS, None), 1
)
@vampytest.call_with(
    '\n \n#a', 0, (PARSED_STATE_END | PARSED_STATE_SUCCESS, None), 5
)
@vampytest.call_with(
    ' \n', 1, (PARSED_STATE_END | PARSED_STATE_SUCCESS, None), 2
)
@vampytest.call_with(
    'a', 0, (PARSED_STATE_END | PARSED_STATE_SUCCESS, ('a', None)), 1
)
@vampytest.call_with(
    'a\n', 0, (PARSED_STATE_SUCCESS, ('a', None)), 2
)
@vampytest.call_with(
    '\na', 0, (PARSED_STATE_END | PARSED_STATE_SUCCESS, ('a', None)), 2
)
@vampytest.call_with(
    '\na', 1, (PARSED_STATE_END | PARSED_STATE_SUCCESS, ('a', None)), 2
)
@vampytest.call_with(
    'a #a', 0, (PARSED_STATE_END | PARSED_STATE_SUCCESS, ('a', None)), 4
)
@vampytest.call_with(
    'a #a\n', 0, (PARSED_STATE_SUCCESS, ('a', None)), 5
)
@vampytest.call_with(
    'a =', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, ('a', None)), 3
)
@vampytest.call_with(
    'a = #a', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, ('a', None)), 6
)
@vampytest.call_with(
    'a = b', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, ('a', 'b')), 5
)
@vampytest.call_with(
    'a = b\n', 0, (PARSED_STATE_SUCCESS, ('a', 'b')), 6
)
@vampytest.call_with(
    'a=b', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, ('a', 'b')), 3
)
@vampytest.call_with(
    'a=b\n', 0, (PARSED_STATE_SUCCESS, ('a', 'b')), 4
)
@vampytest.call_with(
    'a=b#a', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, ('a', 'b')), 5
)
@vampytest.call_with(
    'a=b#a\n', 0, (PARSED_STATE_SUCCESS, ('a', 'b')), 6
)
@vampytest.call_with(
    'a=b ', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, ('a', 'b')), 4
)
@vampytest.call_with(
    'a=b \n', 0, (PARSED_STATE_SUCCESS, ('a', 'b')), 5
)
@vampytest.call_with(
    'a=b c', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, ('a', 'b c')), 5
)
@vampytest.call_with(
    '1 = #a', 0, (embed_error_code(PARSED_STATE_FAILURE, ERROR_CODE_KEY_STARTER_INVALID), None), 0
)
@vampytest.call_with(
    '""', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, None), 2
)
@vampytest.call_with(
    '""=b', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, None), 4
)
@vampytest.call_with(
    '"a"=b', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, ('a', 'b')), 5
)
@vampytest.call_with(
    '"a"="b"', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, ('a', 'b')), 7
)
@vampytest.call_with(
    'a="b~"', 0, (PARSED_STATE_SUCCESS | PARSED_STATE_END, ('a', 'b~')), 6
)
@vampytest.call_with(
    'a="b" a', 0, (embed_error_code(PARSED_STATE_FAILURE, ERROR_CODE_VALUE_ALREADY_PARSED), ('a', 'b')), 6
)
@vampytest.call_with(
    '"a" "c"=b', 0, (embed_error_code(PARSED_STATE_FAILURE, ERROR_CODE_EXPECTED_EQUAL_SIGN), ('a', None)), 4
)
@vampytest.call_with(
    'a=b\nc=d', 0, (PARSED_STATE_SUCCESS, ('a', 'b')), 4
)
@vampytest.call_with(
    'a=b\nc=d', 4, (PARSED_STATE_SUCCESS | PARSED_STATE_END, ('c', 'd')), 7
)
def test__parse_item(value, position, expected_output, expected_position):
    """
    Tests whether ``parse_item`` works as intended.
    Parameters
    ----------
    value : `str`
        Value to parse.
    position : `int`
        The position to start parsing at.
    expected_output : `tuple` (`int`, `str` | `tuple`(`str`, `None` | `str`))
        The expected output to be returned.
    expected_position : `int`
        The expected position of the parser after parsing the item.
    """
    state = ParserState(value)
    state.position = position
    
    output = parse_item(state)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(state.position, expected_position)
