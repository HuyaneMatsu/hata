import vampytest

from ..fields import put_boost_progress_bar_enabled


def test__put_boost_progress_bar_enabled():
    """
    Tests whether ``put_boost_progress_bar_enabled`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'premium_progress_bar_enabled': False}),
        (True, False, {'premium_progress_bar_enabled': True}),
    ):
        data = put_boost_progress_bar_enabled(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
