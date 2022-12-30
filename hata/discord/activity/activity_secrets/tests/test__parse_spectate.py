import vampytest

from ..fields import parse_spectate


def test__parse_spectate():
    """
    Tests whether ``parse_spectate`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'spectate': None}, None),
        ({'spectate': ''}, None),
        ({'spectate': 'a'}, 'a'),
    ):
        output = parse_spectate(input_data)
        vampytest.assert_eq(output, expected_output)
