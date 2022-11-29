import vampytest

from ..fields import put_overlay_compatibility_hook_into


def test__put_overlay_compatibility_hook_into():
    """
    Tests whether ``put_overlay_compatibility_hook_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'overlay_compatibility_hook': False}),
        (True, False, {'overlay_compatibility_hook': True}),
    ):
        data = put_overlay_compatibility_hook_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
