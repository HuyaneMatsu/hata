import vampytest

from ..preinstanced import VerificationScreenStepType
from ..verification_screen_step import VerificationScreenStep

from .test__VerificationScreenStep__constructor import _check_is_every_field_set


def test__VerificationScreenStep__from_data():
    """
    Tests whether ``VerificationScreenStep.from_data`` works as intended.
    """
    required = True
    title = 'Yukari'
    step_type = VerificationScreenStepType.text_input
    values = ['kisaki']
    
    data = {
        'required': required,
        'label': title,
        'field_type': step_type.value,
        'values': values,
    }
    
    verification_screen_step = VerificationScreenStep.from_data(data)
    _check_is_every_field_set(verification_screen_step)
    
    vampytest.assert_eq(verification_screen_step.required, required)
    vampytest.assert_eq(verification_screen_step.title, title)
    vampytest.assert_eq(verification_screen_step.type, step_type)
    vampytest.assert_eq(verification_screen_step.values, tuple(values))


def test__VerificationScreenStep__to_data():
    """
    Tests whether ``VerificationScreenStep.to_data`` works as intended.
    
    Case: include defaults.
    """
    required = True
    title = 'Yukari'
    step_type = VerificationScreenStepType.text_input
    values = ['kisaki']
    
    expected_data = {
        'required': required,
        'label': title,
        'field_type': step_type.value,
        'values': values,
    }
    
    verification_screen_step = VerificationScreenStep(
        required = required,
        title = title,
        step_type = step_type,
        values = values,
    )
    
    vampytest.assert_eq(
        verification_screen_step.to_data(defaults = True),
        expected_data,
    )
