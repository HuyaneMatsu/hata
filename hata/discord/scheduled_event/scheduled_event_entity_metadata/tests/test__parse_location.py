import vampytest

from ..fields import parse_location


def test__parse_location():
    """
    Tests whether ``parse_location`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'location': None}, None),
        ({'location': ''}, None),
        ({'location': 'a'}, 'a'),
    ):
        output = parse_location(input_data)
        vampytest.assert_eq(output, expected_output)
