import vampytest

from ..fields import put_key_into


def test__put_key_into():
    """
    Tests whether ``put_key_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        ('', False, {'key': ''}),
        ('a', False, {'key': 'a'}),
    ):
        data = put_key_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
