import vampytest

from ..fields import put_duration_into


def test__put_duration_into():
    """
    Tests whether ``put_duration_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (0.0, False, {}),
        (0.0, True, {'duration_sec': 0.0}),
        (1.0, False, {'duration_sec': 1.0}),
    ):
        data = put_duration_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
