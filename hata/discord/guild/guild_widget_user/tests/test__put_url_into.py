import vampytest

from ..fields import put_avatar_url


def test__put_avatar_url():
    """
    Tests whether ``put_avatar_url`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('https://orindance.party/', False, {'avatar_url': 'https://orindance.party/'}),
    ):
        data = put_avatar_url(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
