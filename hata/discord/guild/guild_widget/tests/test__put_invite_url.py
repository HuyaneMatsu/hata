import vampytest

from ..fields import put_invite_url


def test__put_invite_url():
    """
    Tests whether ``put_invite_url`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('https://orindance.party/', False, {'instant_invite': 'https://orindance.party/'}),
    ):
        data = put_invite_url(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
