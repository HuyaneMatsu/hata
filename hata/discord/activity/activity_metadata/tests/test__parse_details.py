import vampytest

from ..fields import parse_details


def test__parse_details():
    """
    Tests whether ``parse_details`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'details': None}, None),
        ({'details': ''}, None),
        ({'details': 'a'}, 'a'),
    ):
        output = parse_details(input_data)
        vampytest.assert_eq(output, expected_output)
