import vampytest

from ..fields import parse_proxy_url


def test__parse_proxy_url():
    """
    Tests whether ``parse_proxy_url`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'proxy_url': None}, None),
        ({'proxy_url': ''}, None),
        ({'proxy_url': 'https://orindance.party/'}, 'https://orindance.party/'),
    ):
        output = parse_proxy_url(input_data)
        vampytest.assert_eq(output, expected_output)
