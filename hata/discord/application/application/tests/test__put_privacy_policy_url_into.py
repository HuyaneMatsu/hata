import vampytest

from ..fields import put_privacy_policy_url_into


def test__put_privacy_policy_url_into():
    """
    Tests whether ``put_privacy_policy_url_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        ('https://orindance.party/', False, {'privacy_policy_url': 'https://orindance.party/'}),
    ):
        data = put_privacy_policy_url_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
