import vampytest

from ..fields import parse_options
from ..interaction_option import InteractionOption


def test__parse_options():
    """
    Tests whether ``parse_options`` works as intended.
    """
    option = InteractionOption(name = 'requiem')
    
    for input_data, expected_output in (
        ({}, None),
        ({'options': None}, None),
        ({'options': []}, None),
        ({'options': [option.to_data()]}, (option, )),
    ):
        output = parse_options(input_data)
        vampytest.assert_eq(output, expected_output)
