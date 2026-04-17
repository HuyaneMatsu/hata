import vampytest

from ..preinstanced import VerificationScreenStepType
from ..verification_screen_step import VerificationScreenStep


def test__VerificationScreenStep__repr():
    """
    Tests whether ``VerificationScreenStep.__repr__`` works as intended.
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
    vampytest.assert_instance(repr(verification_screen_step), str)


def test__VerificationScreenStep__hash():
    """
    Tests whether ``VerificationScreenStep.__hash__`` works as intended.
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
    vampytest.assert_instance(hash(verification_screen_step), int)


def test__VerificationScreenStep__eq():
    """
    Tests whether ``VerificationScreenStep.__eq__`` works as intended.
    """
    required = True
    title = 'Yukari'
    step_type = VerificationScreenStepType.text_input
    values = ['kisaki']
    
    keyword_parameters = {
        'required': required,
        'title': title,
        'step_type': step_type,
        'values': values,
    }
    
    verification_screen_step = VerificationScreenStep(**keyword_parameters)
    vampytest.assert_eq(verification_screen_step, verification_screen_step)
    vampytest.assert_ne(verification_screen_step, object())
    
    for field_name, field_value in (
        ('required', False),
        ('title', 'Yurica'),
        ('step_type', VerificationScreenStepType.paragraph),
        ('values', None),
    ):
        test_verification_screen_step = VerificationScreenStep(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(verification_screen_step, test_verification_screen_step)
