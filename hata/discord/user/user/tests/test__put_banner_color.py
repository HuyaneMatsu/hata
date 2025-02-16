import vampytest

from ..fields import put_banner_color


def test__put_banner_color():
    """
    Tests whether ``put_banner_color`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'accent_color': None}),
        (0, False, {'accent_color': 0}),
    ):
        data = put_banner_color(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
