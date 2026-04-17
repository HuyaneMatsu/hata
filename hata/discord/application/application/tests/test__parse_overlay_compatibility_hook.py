import vampytest

from ..fields import parse_overlay_compatibility_hook


def test__parse_overlay_compatibility_hook():
    """
    Tests whether ``parse_overlay_compatibility_hook`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'overlay_compatibility_hook': False}, False),
        ({'overlay_compatibility_hook': True}, True),
    ):
        output = parse_overlay_compatibility_hook(input_data)
        vampytest.assert_eq(output, expected_output)
