import vampytest

from ..parsing import parse_variables


@vampytest.call_with('', ({}, -1))
@vampytest.call_with('a=b', ({'a': 'b'}, -1))
@vampytest.call_with('a', ({'a': None}, -1))
@vampytest.call_with('a=b\nc', ({'a': 'b', 'c': None}, -1))
@vampytest.call_with('c=d\n12', ({'c': 'd'}, 5))
def test__parse_variables(input_value, expected_output):
    """
    Tests whether `parse_variables`` works as intended.
    """
    output = parse_variables(input_value)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(output, expected_output)
