import vampytest

from ..fields import parse_tags


def test__parse_parse_tags():
    """
    Tests whether ``parse_tags`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'tags': None}, None),
        ({'tags': ''}, None),
        ({'tags': 'lost'}, frozenset(('lost', ))),
        ({'tags': 'lost, emotion'}, frozenset(('lost', 'emotion'))),   
    ):
        output = parse_tags(input_data)
        vampytest.assert_eq(output, expected_output)
