import vampytest

from ...verification_screen_step import VerificationScreenStep, VerificationScreenStepType

from ..fields import parse_steps


def test__parse_steps():
    """
    Tests whether `parse_steps` works as intended.
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
    
    for input_data, expected_output in (
        ({}, None),
        ({'form_fields': None}, None),
        ({'form_fields': []}, None),
        (
            {'form_fields': [verification_screen_step_0.to_data(defaults = True)]},
            (verification_screen_step_0, ),
        ),
        (
            {
                'form_fields': [
                    verification_screen_step_0.to_data(defaults = True),
                    verification_screen_step_1.to_data(defaults = True),
                ],
            },
            (verification_screen_step_0, verification_screen_step_1),
        ),
    ):
        output = parse_steps(input_data)
        vampytest.assert_eq(output, expected_output)
