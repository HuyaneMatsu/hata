import vampytest

from ..fields import parse_avatar_url


def test__parse_avatar_url():
    """
    Tests whether ``parse_avatar_url`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ''),
        ({'avatar_url': None}, ''),
        ({'avatar_url': ''}, ''),
        ({'avatar_url': 'https://orindance.party/'}, 'https://orindance.party/'),
    ):
        output = parse_avatar_url(input_data)
        vampytest.assert_eq(output, expected_output)
