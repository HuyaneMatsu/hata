import vampytest

from ..fields import put_overlay_compatibility_hook


def test__put_overlay_compatibility_hook():
    """
    Tests whether ``put_overlay_compatibility_hook`` works as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'overlay_compatibility_hook': False}),
        (True, False, {'overlay_compatibility_hook': True}),
    ):
        data = put_overlay_compatibility_hook(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
