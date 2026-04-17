import vampytest

from ..fields import put_icon_url


def test__put_icon_url():
    """
    Tests whether ``put_icon_url`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('https://orindance.party/', False, {'icon_url': 'https://orindance.party/'}),
    ):
        data = put_icon_url(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
