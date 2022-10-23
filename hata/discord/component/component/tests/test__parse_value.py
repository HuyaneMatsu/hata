import vampytest

from ..fields import parse_value


def test__parse_value():
    """
    Tests whether ``parse_value`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'value': None}, None),
        ({'value': ''}, None),
        ({'value': 'a'}, 'a'),
    ):
        output = parse_value(input_data)
        vampytest.assert_eq(output, expected_output)
