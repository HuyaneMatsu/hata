import vampytest

from ..fields import put_widget_channel_id_into


def test__put_widget_channel_id_into():
    """
    Tests whether ``put_widget_channel_id_into`` works as intended.
    """
    widget_channel_id = 202306150023
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'widget_channel_id': None}),
        (widget_channel_id, False, {'widget_channel_id': str(widget_channel_id)}),
    ):
        data = put_widget_channel_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
