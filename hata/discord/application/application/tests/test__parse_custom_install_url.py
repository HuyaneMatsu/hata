import vampytest

from ..fields import parse_custom_install_url


def test__parse_custom_install_url():
    """
    Tests whether ``parse_custom_install_url`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'custom_install_url': None}, None),
        ({'custom_install_url': ''}, None),
        ({'custom_install_url': 'https://orindance.party/'}, 'https://orindance.party/'),
    ):
        output = parse_custom_install_url(input_data)
        vampytest.assert_eq(output, expected_output)
