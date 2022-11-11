import vampytest

from ..fields import parse_content_type


def test__parse_content_type():
    """
    Tests whether ``parse_content_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'content_type': None}, None),
        ({'content_type': ''}, None),
        ({'content_type': 'a'}, 'a'),
    ):
        output = parse_content_type(input_data)
        vampytest.assert_eq(output, expected_output)
