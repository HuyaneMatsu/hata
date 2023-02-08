import vampytest

from ..fields import put_email_into


def test__put_email_into():
    """
    Tests whether ``put_email_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        ('meow', False, {'email': 'meow'}),
    ):
        data = put_email_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
