import vampytest

from ..fields import put_verify_key_into


def test__put_verify_key_into():
    """
    Tests whether ``put_verify_key_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'verify_key': ''}),
        ('', False, {'verify_key': ''}),
        ('a', False, {'verify_key': 'a'}),
    ):
        data = put_verify_key_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
