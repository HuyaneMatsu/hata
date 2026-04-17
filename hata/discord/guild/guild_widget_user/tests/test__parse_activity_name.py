import vampytest

from ..fields import parse_activity_name


def test__parse_activity_name():
    """
    Tests whether ``parse_activity_name`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'game': None}, None),
        ({'game': {}}, None),
        ({'game': {'name': None}}, None),
        ({'game': {'name': ''}}, None),
        ({'game': {'name': 'a'}}, 'a'),
    ):
        output = parse_activity_name(input_data)
        vampytest.assert_eq(output, expected_output)
