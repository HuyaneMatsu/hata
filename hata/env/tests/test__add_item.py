import vampytest

from ..parsing import add_item


@vampytest.call_with({}, None, False, {})
@vampytest.call_with({}, ('a', 'b'), True, {'a': 'b'})
@vampytest.call_with({}, ('a', None), True, {'a': None})
@vampytest.call_with({'a': 'c'}, ('a', 'b'), False, {'a': 'c'})
@vampytest.call_with({'a': None}, ('a', 'b'), True, {'a': 'b'})
def test__add_item(input_variables, input_item, expected_output, expected_variables):
    """
    Tests whether `add_item`` works as intended.
    """
    variables = input_variables.copy()
    output = add_item(variables, input_item)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(variables, expected_variables)
