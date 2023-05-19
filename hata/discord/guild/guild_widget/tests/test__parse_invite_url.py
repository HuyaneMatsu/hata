import vampytest

from ..fields import parse_invite_url


def test__parse_invite_url():
    """
    Tests whether ``parse_invite_url`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'instant_invite': None}, None),
        ({'instant_invite': ''}, None),
        ({'instant_invite': 'https://orindance.party/'}, 'https://orindance.party/'),
    ):
        output = parse_invite_url(input_data)
        vampytest.assert_eq(output, expected_output)
