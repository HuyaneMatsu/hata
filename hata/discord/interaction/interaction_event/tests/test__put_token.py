import vampytest

from ..fields import put_token


def test__put_token():
    """
    Tests whether ``put_token`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        ('', False, {'token': ''}),
        ('a', False, {'token': 'a'}),
    ):
        data = put_token(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
