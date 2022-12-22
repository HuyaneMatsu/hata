import vampytest

from ..preinstanced import VerificationScreenStepType
from ..verification_screen_step import VerificationScreenStep

from .test__VerificationScreenStep__constructor import _check_is_every_field_set


def test__VerificationScreenStep__new__copy():
    """
    Tests whether ``VerificationScreenStep.copy`` works as intended.
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
    copy = verification_screen_step.copy()
    _check_is_every_field_set(copy)
    
    vampytest.assert_eq(verification_screen_step, copy)
    vampytest.assert_is_not(verification_screen_step, copy)


def test__VerificationScreenStep__new__copy_with__0():
    """
    Tests whether ``VerificationScreenStep.copy_with`` works as intended.
    
    Case: No fields given.
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
    copy = verification_screen_step.copy_with()
    _check_is_every_field_set(copy)
    
    vampytest.assert_eq(verification_screen_step, copy)
    vampytest.assert_is_not(verification_screen_step, copy)


def test__VerificationScreenStep__new__copy_with__1():
    """
    Tests whether ``VerificationScreenStep.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_required = True
    new_required = False
    old_title = 'Yukari'
    new_title = 'Yurica'
    old_step_type = VerificationScreenStepType.text_input
    new_step_type = VerificationScreenStepType.paragraph
    old_values = ['kisaki']
    new_values = ['nasca']
    
    verification_screen_step = VerificationScreenStep(
        required = old_required,
        title = old_title,
        step_type = old_step_type,
        values = old_values,
    )
    copy = verification_screen_step.copy_with(
        required = new_required,
        title = new_title,
        step_type = new_step_type,
        values = new_values,
    )
    _check_is_every_field_set(copy)
    
    vampytest.assert_is_not(verification_screen_step, copy)
    
    vampytest.assert_eq(copy.required, new_required)
    vampytest.assert_eq(copy.title, new_title)
    vampytest.assert_eq(copy.type, new_step_type)
    vampytest.assert_eq(copy.values, tuple(new_values))


def test__VerificationScreenStep__iter_values():
    """
    Asserts whether ``VerificationScreenStep.iter_values`` works as intended.
    """
    for input_value, expected_output in (
        (None, []),
        (['a'], ['a']),
        (['a', 'b'], ['a', 'b']),
    ):
        verification_screen_step = VerificationScreenStep(values = input_value)
        vampytest.assert_eq(expected_output, [*verification_screen_step.iter_values()])
