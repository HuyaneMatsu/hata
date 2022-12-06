import vampytest

from ..fields import parse_platform_user_name


def test__parse_platform_user_name():
    """
    Tests whether ``parse_platform_user_name`` works as intended.
    """
    for input_data, expected_output in (
        ({'platform_username': None}, None),
        ({'platform_username': ''}, None),
        ({'platform_username': 'a'}, 'a'),
    ):
        output = parse_platform_user_name(input_data)
        vampytest.assert_eq(output, expected_output)
