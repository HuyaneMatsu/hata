import vampytest

from ..default_thread_slowmode import validate_default_thread_slowmode


def test__validate_default_thread_slowmode():
    """
    Validates whether ``validate_default_thread_slowmode`` works as intended.
    """
    for input_value, expected_output in (
        (0, 0),
    ):
        output = validate_default_thread_slowmode(input_value)
        vampytest.assert_eq(output, expected_output)
