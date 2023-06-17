import vampytest

from ..fields import parse_widget_channel_id


def test__parse_widget_channel_id():
    """
    Tests whether ``parse_widget_channel_id`` works as intended.
    """
    widget_channel_id = 202306150024
    
    for input_data, expected_output in (
        ({}, 0),
        ({'widget_channel_id': None}, 0),
        ({'widget_channel_id': str(widget_channel_id)}, widget_channel_id),
    ):
        output = parse_widget_channel_id(input_data)
        vampytest.assert_eq(output, expected_output)
