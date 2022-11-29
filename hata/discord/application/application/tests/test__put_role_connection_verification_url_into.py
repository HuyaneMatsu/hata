import vampytest

from ..fields import put_role_connection_verification_url_into


def test__put_role_connection_verification_url_into():
    """
    Tests whether ``put_role_connection_verification_url_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        ('https://orindance.party/', False, {'role_connections_verification_url': 'https://orindance.party/'}),
    ):
        data = put_role_connection_verification_url_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
