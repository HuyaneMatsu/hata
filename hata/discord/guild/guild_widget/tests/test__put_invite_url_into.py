import vampytest

from ..fields import put_invite_url_into


def test__put_invite_url_into():
    """
    Tests whether ``put_invite_url_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('https://orindance.party/', False, {'instant_invite': 'https://orindance.party/'}),
    ):
        data = put_invite_url_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
