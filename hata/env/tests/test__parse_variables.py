import vampytest

from ..parsing import ERROR_CODE_KEY_STARTER_INVALID, ERROR_CODE_QUOTE_NOT_CLOSED, ParserFailureInfo, parse_variables


@vampytest.call_with('', ({}, None))
@vampytest.call_with('a=b', ({'a': 'b'}, None))
@vampytest.call_with('a', ({'a': None}, None))
@vampytest.call_with('a=b\nc', ({'a': 'b', 'c': None}, None))
@vampytest.call_with('c=d\n12', ({'c': 'd'}, ParserFailureInfo(0, '12', 1, ERROR_CODE_KEY_STARTER_INVALID)))
@vampytest.call_with('a=\'aya', ({'a': None}, ParserFailureInfo(6, 'a=\'aya', 0, ERROR_CODE_QUOTE_NOT_CLOSED)))
def test__parse_variables(input_value, expected_output):
    """
    Tests whether `parse_variables`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to parse.
    expected_output : `(dict<str, None | str>, None | ParserFailureInfo)
        The expected output returned by the variable parser.`
    """
    output = parse_variables(input_value)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, expected_output)
