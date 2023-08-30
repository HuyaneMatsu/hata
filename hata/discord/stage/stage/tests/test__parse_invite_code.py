import vampytest

from ..fields import parse_invite_code


def test__parse_invite_code():
    """
    Tests whether ``parse_invite_code`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'invite_code': None}, None),
        ({'invite_code': ''}, None),
        ({'invite_code': 'a'}, 'a'),
    ):
        output = parse_invite_code(input_data)
        vampytest.assert_eq(output, expected_output)
