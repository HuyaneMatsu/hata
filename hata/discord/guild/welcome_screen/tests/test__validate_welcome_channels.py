import vampytest

from ...welcome_screen_channel import WelcomeScreenChannel

from ..fields import validate_welcome_channels


def test__validate_welcome_channels__0():
    """
    Tests whether `validate_welcome_channels` works as intended.
    
    Case: Passing.
    """
    welcome_screen_channel_0 = WelcomeScreenChannel(
        description = 'Yukari',
    )
    
    welcome_screen_channel_1 = WelcomeScreenChannel(
        description = 'Yurica',
    )
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([welcome_screen_channel_0], (welcome_screen_channel_0,),),
        (
            [welcome_screen_channel_0, welcome_screen_channel_1],
            (welcome_screen_channel_0, welcome_screen_channel_1),
        ),
    ):
        output = validate_welcome_channels(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_welcome_channels__1():
    """
    Tests whether `validate_welcome_channels` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_welcome_channels(input_value)
