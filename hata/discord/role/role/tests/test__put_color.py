import vampytest

from ....color import Color

from ..fields import put_color


def test__put_color():
    """
    Tests whether ``put_color`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (Color(0), False, {}),
        (Color(0), True, {'color': 0}),
        (Color(1), False, {'color': 1}),
    ):
        data = put_color(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
