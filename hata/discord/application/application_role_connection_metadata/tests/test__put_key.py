import vampytest

from ..fields import put_key


def test__put_key():
    """
    Tests whether ``put_key`` works as intended.
    """
    for input_, defaults, expected_output in (
        ('', False, {'key': ''}),
        ('a', False, {'key': 'a'}),
    ):
        data = put_key(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
