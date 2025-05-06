import vampytest

from ..fields import put_platform_user_name


def test__put_platform_user_name():
    """
    Tests whether ``put_platform_user_name`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'platform_username': ''}),
        ('', False, {'platform_username': ''}),
        ('a', False, {'platform_username': 'a'}),
    ):
        data = put_platform_user_name(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
