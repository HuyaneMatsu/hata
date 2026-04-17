import vampytest

from ..fields import put_refresh_token


def test__put_refresh_token():
    """
    Tests whether ``put_refresh_token`` works as intended.
    """
    for input_value, defaults, expected_output in (
        ('', False, {'refresh_token': ''}),
        ('a', False, {'refresh_token': 'a'}),
    ):
        data = put_refresh_token(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
