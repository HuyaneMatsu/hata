import vampytest

from ..preinstanced import VerificationScreenStepType
from ..verification_screen_step import VerificationScreenStep


def _check_is_every_field_set(verification_screen_step):
    """
    Asserts whether all fields are set of the given verification_screen_step.
    
    Parameters
    ----------
    verification_screen_step : ``VerificationScreenStep``
        The guild verification_screen_step instance to check.
    """
    vampytest.assert_instance(verification_screen_step, VerificationScreenStep)
    vampytest.assert_instance(verification_screen_step.required, bool)
    vampytest.assert_instance(verification_screen_step.title, str)
    vampytest.assert_instance(verification_screen_step.type, VerificationScreenStepType)
    vampytest.assert_instance(verification_screen_step.values, tuple, nullable = True)



def test__VerificationScreenStep__new__0():
    """
    Tests whether ``VerificationScreenStep.__new__`` works as intended.
    
    Case: No fields given.
    """
    verification_screen_step = VerificationScreenStep()
    _check_is_every_field_set(verification_screen_step)


def test__VerificationScreenStep__new__1():
    """
    Tests whether ``VerificationScreenStep.__new__`` works as intended.
    
    Case: All fields given.
    """
    required = True
    title = 'Yukari'
    step_type = VerificationScreenStepType.text_input
    values = ['kisaki']
    
    verification_screen_step = VerificationScreenStep(
        required = required,
        title = title,
        step_type = step_type,
        values = values,
    )
    _check_is_every_field_set(verification_screen_step)
    
    vampytest.assert_eq(verification_screen_step.required, required)
    vampytest.assert_eq(verification_screen_step.title, title)
    vampytest.assert_is(verification_screen_step.type, step_type)
    vampytest.assert_eq(verification_screen_step.values, tuple(values))
