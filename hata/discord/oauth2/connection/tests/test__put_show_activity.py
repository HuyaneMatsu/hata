import vampytest

from ..fields import put_show_activity


def test__put_show_activity():
    """
    Tests whether ``put_show_activity`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'show_activity': False}),
        (True, False, {'show_activity': True}),
    ):
        data = put_show_activity(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
