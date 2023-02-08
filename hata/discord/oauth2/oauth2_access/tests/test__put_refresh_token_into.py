import vampytest

from ..fields import put_refresh_token_into


def test__put_refresh_token_into():
    """
    Tests whether ``put_refresh_token_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        ('', False, {'refresh_token': ''}),
        ('a', False, {'refresh_token': 'a'}),
    ):
        data = put_refresh_token_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
