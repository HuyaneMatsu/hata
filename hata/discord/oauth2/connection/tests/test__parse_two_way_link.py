import vampytest

from ..fields import parse_two_way_link


def test__parse_two_way_link():
    """
    Tests whether ``parse_two_way_link`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'two_way_link': False}, False),
        ({'two_way_link': True}, True),
    ):
        output = parse_two_way_link(input_data)
        vampytest.assert_eq(output, expected_output)
