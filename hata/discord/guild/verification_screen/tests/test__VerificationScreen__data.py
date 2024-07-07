from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ...verification_screen_step import VerificationScreenStep, VerificationScreenStepType

from ..verification_screen import VerificationScreen

from .test__VerificationScreen__constructor import _check_is_every_field_set


def test__VerificationScreen__from_data():
    """
    Tests whether ``VerificationScreen.from_data`` works as intended.
    """
    edited_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    description = 'Yukari'
    steps = [
        VerificationScreenStep(
            required = True,
            title = 'Yukari',
            step_type = VerificationScreenStepType.text_input,
            values = ['kisaki'],
        ),
    ]
    
    data = {
        'version': datetime_to_timestamp(edited_at),
        'description': description,
        'form_fields': [step.to_data(defaults = True) for step in steps],
    }
    
    verification_screen = VerificationScreen.from_data(data)
    _check_is_every_field_set(verification_screen)
    
    vampytest.assert_eq(verification_screen.edited_at, edited_at)
    vampytest.assert_eq(verification_screen.description, description)
    vampytest.assert_eq(verification_screen.steps, tuple(steps))


def test__VerificationScreen__to_data():
    """
    Tests whether ``VerificationScreen.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    edited_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    description = 'Yukari'
    steps = [
        VerificationScreenStep(
            required = True,
            title = 'Yukari',
            step_type = VerificationScreenStepType.text_input,
            values = ['kisaki'],
        ),
    ]
    
    expected_data = {
        'version': datetime_to_timestamp(edited_at),
        'description': description,
        'form_fields': [step.to_data(defaults = True) for step in steps],
    }
    
    verification_screen = VerificationScreen(
        edited_at = edited_at,
        description = description,
        steps = steps,
    )
    
    vampytest.assert_eq(
        verification_screen.to_data(defaults = True, include_internals = True),
        expected_data,
    )
