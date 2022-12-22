from datetime import datetime as DateTime

import vampytest

from ...verification_screen_step import VerificationScreenStep, VerificationScreenStepType

from ..verification_screen import VerificationScreen

from .test__VerificationScreen__constructor import _check_is_every_field_set


def test__VerificationScreen__new__copy():
    """
    Tests whether ``VerificationScreen.copy`` works as intended.
    """
    edited_at = DateTime(2016, 5, 14)
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
    copy = verification_screen.copy()
    _check_is_every_field_set(copy)
    
    vampytest.assert_eq(verification_screen, copy)
    vampytest.assert_is_not(verification_screen, copy)


def test__VerificationScreen__new__copy_with__0():
    """
    Tests whether ``VerificationScreen.copy_with`` works as intended.
    
    Case: No fields given.
    """
    edited_at = DateTime(2016, 5, 14)
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
    copy = verification_screen.copy_with()
    _check_is_every_field_set(copy)
    
    vampytest.assert_eq(verification_screen, copy)
    vampytest.assert_is_not(verification_screen, copy)


def test__VerificationScreen__new__copy_with__1():
    """
    Tests whether ``VerificationScreen.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_edited_at = DateTime(2016, 5, 14)
    new_edited_at = DateTime(2017, 5, 14)
    old_description = 'Yukari'
    new_description = 'Yurica'
    old_steps = [
        VerificationScreenStep(
            required = True,
            title = 'Yukari',
            step_type = VerificationScreenStepType.text_input,
            values = ['kisaki'],
        ),
    ]
    new_steps = [
        VerificationScreenStep(
            required = True,
            title = 'Yukari',
            step_type = VerificationScreenStepType.text_input,
            values = ['kisaki'],
        ),
        VerificationScreenStep(
            required = False,
            title = 'Yurica',
            step_type = VerificationScreenStepType.rules,
            values = ['Nasca'],
        ),
    ]
    
    verification_screen = VerificationScreen(
        edited_at = old_edited_at,
        description = old_description,
        steps = old_steps,
    )
    copy = verification_screen.copy_with(
        edited_at = new_edited_at,
        description = new_description,
        steps = new_steps,
    )
    _check_is_every_field_set(copy)
    
    vampytest.assert_is_not(verification_screen, copy)
    
    vampytest.assert_eq(copy.edited_at, new_edited_at)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.steps, tuple(new_steps))


def test__VerificationScreen__iter_steps():
    """
    Asserts whether ``VerificationScreen.iter_steps`` works as intended.
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
        (None, []),
        ([verification_screen_step_0], [verification_screen_step_0]),
        (
            [verification_screen_step_0, verification_screen_step_1],
            [verification_screen_step_0, verification_screen_step_1],
        ),
    ):
        verification_screen = VerificationScreen(steps = input_value)
        vampytest.assert_eq(expected_output, [*verification_screen.iter_steps()])
