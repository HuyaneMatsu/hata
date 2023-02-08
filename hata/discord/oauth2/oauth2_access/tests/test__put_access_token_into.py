import vampytest

from ..fields import put_access_token_into


def test__put_access_token_into():
    """
    Tests whether ``put_access_token_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        ('', False, {'access_token': ''}),
        ('a', False, {'access_token': 'a'}),
    ):
        data = put_access_token_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
