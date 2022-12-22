import vampytest

from ...verification_screen_step import VerificationScreenStep, VerificationScreenStepType

from ..fields import validate_steps


def test__validate_steps__0():
    """
    Tests whether `validate_steps` works as intended.
    
    Case: Passing.
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
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([verification_screen_step_0], (verification_screen_step_0,),),
        (
            [verification_screen_step_0, verification_screen_step_1],
            (verification_screen_step_0, verification_screen_step_1),
        ),
    ):
        output = validate_steps(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_steps__1():
    """
    Tests whether `validate_steps` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_steps(input_value)
