import vampytest

from ..fields import parse_parameters


def test__parse_parameters():
    """
    Tests whether ``parse_parameters`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'parameters': None}, None),
        ({'parameters': ''}, None),
        ({'parameters': 'a'}, 'a'),
    ):
        output = parse_parameters(input_data)
        vampytest.assert_eq(output, expected_output)
