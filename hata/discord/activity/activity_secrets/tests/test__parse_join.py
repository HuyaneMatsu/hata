import vampytest

from ..fields import parse_join


def test__parse_join():
    """
    Tests whether ``parse_join`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'join': None}, None),
        ({'join': ''}, None),
        ({'join': 'a'}, 'a'),
    ):
        output = parse_join(input_data)
        vampytest.assert_eq(output, expected_output)
