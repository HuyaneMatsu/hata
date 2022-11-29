import vampytest

from ..fields import parse_aliases


def test__parse_aliases():
    """
    Tests whether ``parse_aliases`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'aliases': None}, None),
        ({'aliases': []}, None),
        ({'aliases': ['a']}, ('a', )),
    ):
        output = parse_aliases(input_data)
        vampytest.assert_eq(output, expected_output)
