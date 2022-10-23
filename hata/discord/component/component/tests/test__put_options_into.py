import vampytest

from ...string_select_option import StringSelectOption
from ..fields import put_options_into


def test__put_options_into():
    """
    Tests whether ``put_options_into`` works as intended.
    """
    option = StringSelectOption('hello')
    
    for input_value, expected_output in (
        (None, {'options': []}),
        ((option, ), {'options': [option.to_data(defaults = True)]}),
    ):
        output = put_options_into(input_value, {}, True)
        vampytest.assert_eq(output, expected_output)
