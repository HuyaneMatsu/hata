import vampytest

from ...activity_secrets import ActivitySecrets

from ..fields import put_secrets_into


def test__put_secrets_into():
    """
    Tests whether ``put_secrets_into`` is working as intended.
    """
    secrets = ActivitySecrets(join = 'hell')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (secrets, False, {'secrets': secrets.to_data()}),
        (secrets, True, {'secrets': secrets.to_data(defaults = True)}),
    ):
        data = put_secrets_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
