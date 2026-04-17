import vampytest

from ..fields import parse_distributor


def test__parse_distributor():
    """
    Tests whether ``parse_distributor`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ''),
        ({'distributor': None}, ''),
        ({'distributor': ''}, ''),
        ({'distributor': 'a'}, 'a'),
    ):
        output = parse_distributor(input_data)
        vampytest.assert_eq(output, expected_output)
