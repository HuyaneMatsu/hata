import vampytest

from ..fields import parse_role_connection_verification_url


def test__parse_role_connection_verification_url():
    """
    Tests whether ``parse_role_connection_verification_url`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'role_connections_verification_url': None}, None),
        ({'role_connections_verification_url': ''}, None),
        ({'role_connections_verification_url': 'https://orindance.party/'}, 'https://orindance.party/'),
    ):
        output = parse_role_connection_verification_url(input_data)
        vampytest.assert_eq(output, expected_output)
