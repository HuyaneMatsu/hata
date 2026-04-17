import vampytest

from ..fields import put_access_token


def test__put_access_token():
    """
    Tests whether ``put_access_token`` works as intended.
    """
    for input_value, defaults, expected_output in (
        ('', False, {'access_token': ''}),
        ('a', False, {'access_token': 'a'}),
    ):
        data = put_access_token(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
