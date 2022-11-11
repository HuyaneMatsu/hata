import vampytest

from ..fields import parse_values


def test__parse_values():
    """
    Tests whether ``parse_values`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'values': None}, None),
        ({'values': []}, None),
        ({'values': ['a']}, ('a', )),
    ):
        output = parse_values(input_data)
        vampytest.assert_eq(output, expected_output)
