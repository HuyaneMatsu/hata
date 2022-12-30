import vampytest

from ..fields import parse_state


def test__parse_state():
    """
    Tests whether ``parse_state`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'state': None}, None),
        ({'state': ''}, None),
        ({'state': 'a'}, 'a'),
    ):
        output = parse_state(input_data)
        vampytest.assert_eq(output, expected_output)
