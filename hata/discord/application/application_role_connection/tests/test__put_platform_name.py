import vampytest

from ..fields import put_platform_name


def test__put_platform_name():
    """
    Tests whether ``put_platform_name`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'platform_name': ''}),
        ('', False, {'platform_name': ''}),
        ('a', False, {'platform_name': 'a'}),
    ):
        data = put_platform_name(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
