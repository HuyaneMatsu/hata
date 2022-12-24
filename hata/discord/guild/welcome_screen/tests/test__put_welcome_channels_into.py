import vampytest

from ...welcome_screen_channel import WelcomeScreenChannel

from ..fields import put_welcome_channels_into


def test__put_welcome_channels_into():
    """
    Tests whether `put_welcome_channels_into` works as intended.
    """
    welcome_screen_channel_0 = WelcomeScreenChannel(
        description = 'Yukari',
    )
    
    welcome_screen_channel_1 = WelcomeScreenChannel(
        description = 'Yurica',
    )
    
    for input_value, defaults, expected_output in (
        (
            None,
            False,
            {},
        ), (
            None,
            True,
            {'welcome_channels': []},
        ), (
            (welcome_screen_channel_0, welcome_screen_channel_1),
            True,
            {
                'welcome_channels': [
                    welcome_screen_channel_0.to_data(defaults = True),
                    welcome_screen_channel_1.to_data(defaults = True),
                ],
            },
        ),
    ):
        output = put_welcome_channels_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
