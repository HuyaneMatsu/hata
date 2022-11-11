import vampytest

from ...color import Color

from ..fields import put_color_into


def test__put_color_into():
    """
    Tests whether ``put_color_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (Color(0), False, {}),
        (Color(0), True, {'color': 0}),
        (Color(1), False, {'color': 1}),
    ):
        data = put_color_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
