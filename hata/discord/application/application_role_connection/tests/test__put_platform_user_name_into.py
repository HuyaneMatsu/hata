import vampytest

from ..fields import put_platform_user_name_into


def test__put_platform_user_name_into():
    """
    Tests whether ``put_platform_user_name_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'platform_username': ''}),
        ('', False, {'platform_username': ''}),
        ('a', False, {'platform_username': 'a'}),
    ):
        data = put_platform_user_name_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
