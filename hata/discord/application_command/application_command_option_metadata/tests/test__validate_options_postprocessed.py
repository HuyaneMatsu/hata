import vampytest

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..fields import validate_options_postprocessed


def test__validate_options_postprocessed__0():
    """
    Tests whether `validate_options_postprocessed` works as intended.
    
    Case: passing.
    """
    option_0 = ApplicationCommandOption('ibuki', 'suika', ApplicationCommandOptionType.integer)
    option_1 = ApplicationCommandOption('ibuki', 'suika', ApplicationCommandOptionType.string)
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([option_0], (option_0, )),
        ([option_0, option_1], (option_0, option_1)),
        ([option_0 for _ in range(30)], (*(option_0 for _ in range(25)),)),
    ):
        output = validate_options_postprocessed(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_options_postprocessed__1():
    """
    Tests whether `validate_options_postprocessed` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_options_postprocessed(input_value)
