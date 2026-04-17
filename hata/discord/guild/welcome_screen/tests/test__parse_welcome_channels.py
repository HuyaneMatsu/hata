import vampytest

from ...welcome_screen_channel import WelcomeScreenChannel

from ..fields import parse_welcome_channels


def test__parse_welcome_channels():
    """
    Tests whether `parse_welcome_channels` works as intended.
    """
    welcome_screen_channel_0 = WelcomeScreenChannel(
        description = 'Yukari',
    )
    
    welcome_screen_channel_1 = WelcomeScreenChannel(
        description = 'Yurica',
    )
    
    for input_data, expected_output in (
        ({}, None),
        ({'welcome_channels': None}, None),
        ({'welcome_channels': []}, None),
        (
            {'welcome_channels': [welcome_screen_channel_0.to_data(defaults = True)]},
            (welcome_screen_channel_0, ),
        ),
        (
            {
                'welcome_channels': [
                    welcome_screen_channel_0.to_data(defaults = True),
                    welcome_screen_channel_1.to_data(defaults = True),
                ],
            },
            (welcome_screen_channel_0, welcome_screen_channel_1),
        ),
    ):
        output = parse_welcome_channels(input_data)
        vampytest.assert_eq(output, expected_output)
