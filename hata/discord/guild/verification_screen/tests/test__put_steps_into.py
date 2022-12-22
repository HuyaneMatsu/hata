import vampytest

from ...verification_screen_step import VerificationScreenStep, VerificationScreenStepType

from ..fields import put_steps_into


def test__put_steps_into():
    """
    Tests whether `put_steps_into` works as intended.
    """
    verification_screen_step_0 = VerificationScreenStep(
        required = True,
        title = 'Yukari',
        step_type = VerificationScreenStepType.text_input,
        values = ['kisaki'],
    )
    
    verification_screen_step_1 = VerificationScreenStep(
        required = False,
        title = 'Yurica',
        step_type = VerificationScreenStepType.rules,
        values = None,
    )
    
    for input_value, defaults, expected_output in (
        (
            None,
            False,
            {},
        ), (
            None,
            True,
            {'form_fields': []},
        ), (
            (verification_screen_step_0, verification_screen_step_1),
            True,
            {
                'form_fields': [
                    verification_screen_step_0.to_data(defaults = True),
                    verification_screen_step_1.to_data(defaults = True),
                ],
            },
        ),
    ):
        output = put_steps_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
