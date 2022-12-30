import vampytest

from ...activity_secrets import ActivitySecrets

from ..fields import parse_secrets


def test__parse_secrets():
    """
    Tests whether ``parse_secrets`` works as intended.
    """
    secrets = ActivitySecrets(join = 'hell')
    
    for input_data, expected_output in (
        ({}, None),
        ({'secrets': None}, None),
        ({'secrets': secrets.to_data()}, secrets),
    ):
        output = parse_secrets(input_data)
        vampytest.assert_eq(output, expected_output)
