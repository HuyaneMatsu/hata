import vampytest

from ..fields import put_overlay_into


def test__put_overlay_into():
    """
    Tests whether ``put_overlay_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'overlay': False}),
        (True, False, {'overlay': True}),
    ):
        data = put_overlay_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
