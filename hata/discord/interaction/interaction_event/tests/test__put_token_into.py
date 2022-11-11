import vampytest

from ..fields import put_token_into


def test__put_token_into():
    """
    Tests whether ``put_token_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        ('', False, {'token': ''}),
        ('a', False, {'token': 'a'}),
    ):
        data = put_token_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
