from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...verification_screen_step import VerificationScreenStep, VerificationScreenStepType

from ..verification_screen import VerificationScreen


def test__VerificationScreen__repr():
    """
    Tests whether ``VerificationScreen.__repr__`` works as intended.
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
    
    verification_screen = VerificationScreen(
        edited_at = edited_at,
        description = description,
        steps = steps,
    )
    vampytest.assert_instance(repr(verification_screen), str)


def test__VerificationScreen__hash():
    """
    Tests whether ``VerificationScreen.__hash__`` works as intended.
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
    
    verification_screen = VerificationScreen(
        edited_at = edited_at,
        description = description,
        steps = steps,
    )
    vampytest.assert_instance(hash(verification_screen), int)


def test__VerificationScreen__eq():
    """
    Tests whether ``VerificationScreen.__eq__`` works as intended.
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
    
    keyword_parameters = {
        'edited_at': edited_at,
        'description': description,
        'steps': steps,
    }
    
    verification_screen = VerificationScreen(**keyword_parameters)
    vampytest.assert_eq(verification_screen, verification_screen)
    vampytest.assert_ne(verification_screen, object())
    
    test_verification_screen = VerificationScreen(**{**keyword_parameters, 'edited_at': edited_at})
    vampytest.assert_eq(verification_screen, test_verification_screen)
    
    for field_name, field_value in (
        ('description', 'Yurica'),
        ('steps', None),
    ):
        test_verification_screen = VerificationScreen(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(verification_screen, test_verification_screen)
