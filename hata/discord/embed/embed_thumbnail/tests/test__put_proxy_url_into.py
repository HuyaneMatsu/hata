import vampytest

from ..fields import put_proxy_url_into


def test__put_proxy_url_into():
    """
    Tests whether ``put_proxy_url_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('https://orindance.party/', False, {'proxy_url': 'https://orindance.party/'}),
    ):
        data = put_proxy_url_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
