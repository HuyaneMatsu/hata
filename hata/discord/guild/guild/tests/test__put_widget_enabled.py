import vampytest

from ..fields import put_widget_enabled


def test__put_widget_enabled():
    """
    Tests whether ``put_widget_enabled`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'widget_enabled': False}),
        (True, False, {'widget_enabled': True}),
    ):
        data = put_widget_enabled(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
