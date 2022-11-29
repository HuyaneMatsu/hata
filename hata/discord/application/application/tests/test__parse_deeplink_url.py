import vampytest

from ..fields import parse_deeplink_url


def test__parse_deeplink_url():
    """
    Tests whether ``parse_deeplink_url`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'deeplink_uri': None}, None),
        ({'deeplink_uri': ''}, None),
        ({'deeplink_uri': 'https://orindance.party/'}, 'https://orindance.party/'),
    ):
        output = parse_deeplink_url(input_data)
        vampytest.assert_eq(output, expected_output)
