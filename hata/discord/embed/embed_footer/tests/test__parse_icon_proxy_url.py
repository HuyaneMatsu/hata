import vampytest

from ..fields import parse_icon_proxy_url


def test__parse_icon_proxy_url():
    """
    Tests whether ``parse_icon_proxy_url`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'proxy_icon_url': None}, None),
        ({'proxy_icon_url': ''}, None),
        ({'proxy_icon_url': 'https://orindance.party/'}, 'https://orindance.party/'),
    ):
        output = parse_icon_proxy_url(input_data)
        vampytest.assert_eq(output, expected_output)
