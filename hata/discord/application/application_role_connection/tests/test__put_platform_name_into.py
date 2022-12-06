import vampytest

from ..fields import put_platform_name_into


def test__put_platform_name_into():
    """
    Tests whether ``put_platform_name_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'platform_name': ''}),
        ('', False, {'platform_name': ''}),
        ('a', False, {'platform_name': 'a'}),
    ):
        data = put_platform_name_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
