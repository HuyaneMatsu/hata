import vampytest

from ..fields import parse_custom_id


def test__parse_custom_id():
    """
    Tests whether ``parse_custom_id`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'custom_id': None}, None),
        ({'custom_id': ''}, None),
        ({'custom_id': 'a'}, 'a'),
    ):
        output = parse_custom_id(input_data)
        vampytest.assert_eq(output, expected_output)
