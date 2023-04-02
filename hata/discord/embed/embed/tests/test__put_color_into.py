import vampytest

from ....color import Color

from ..fields import put_color_into


def test__put_color_into():
    """
    Tests whether ``put_color_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (Color(0), False, {'color': 0}),
        (None, True, {'color': None}),
        (Color(1), False, {'color': 1}),
    ):
        data = put_color_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
