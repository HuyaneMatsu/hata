import vampytest

from ...string_select_option import StringSelectOption

from ..fields import parse_options


def test__parse_options():
    """
    Tests whether ``parse_options`` works as intended.
    """
    option = StringSelectOption('hello')
    
    for input_value, expected_output in (
        ({}, None),
        ({'options': None}, None),
        ({'options': [option.to_data()]}, (option, )),
    ):
        output = parse_options(input_value)
        vampytest.assert_eq(output, expected_output)
