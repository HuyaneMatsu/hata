import vampytest

from ..fields import parse_title


def test__parse_title():
    """
    Tests whether ``parse_title`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'title': None}, None),
        ({'title': ''}, None),
        ({'title': 'a'}, 'a'),
    ):
        output = parse_title(input_data)
        vampytest.assert_eq(output, expected_output)
