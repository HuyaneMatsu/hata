import vampytest

from ...webhook_source_channel import WebhookSourceChannel

from ..fields import validate_source_channel


def test__validate_source_channel__0():
    """
    Tests whether `validate_source_channel` works as intended.
    
    Case: passing.
    """
    channel = WebhookSourceChannel(
        channel_id = 202302020010,
        name = 'itori',
    )
    
    for input_value, expected_output in (
        (None, None),
        (channel, channel),
    ):
        output = validate_source_channel(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_source_channel__1():
    """
    Tests whether `validate_source_channel` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'a',
    ):
        with vampytest.assert_raises(TypeError):
            validate_source_channel(input_value)
