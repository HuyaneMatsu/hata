import vampytest

from ..fields import put_email


def test__put_email():
    """
    Tests whether ``put_email`` works as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        ('meow', False, {'email': 'meow'}),
    ):
        data = put_email(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
