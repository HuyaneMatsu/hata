import vampytest

from ..fields import put_default_thread_slowmode


def test__put_default_thread_slowmode():
    """
    Tests whether ``put_default_thread_slowmode`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'default_thread_rate_limit_per_user': None}),
        (1, False, {'default_thread_rate_limit_per_user': 1}),
    ):
        data = put_default_thread_slowmode(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
