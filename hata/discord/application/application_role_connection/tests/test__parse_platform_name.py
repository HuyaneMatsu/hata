import vampytest

from ..fields import parse_platform_name


def test__parse_platform_name():
    """
    Tests whether ``parse_platform_name`` works as intended.
    """
    for input_data, expected_output in (
        ({'platform_name': None}, None),
        ({'platform_name': ''}, None),
        ({'platform_name': 'a'}, 'a'),
    ):
        output = parse_platform_name(input_data)
        vampytest.assert_eq(output, expected_output)
