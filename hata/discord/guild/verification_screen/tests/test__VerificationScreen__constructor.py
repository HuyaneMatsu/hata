from datetime import datetime as DateTime

import vampytest

from ...verification_screen_step import VerificationScreenStep, VerificationScreenStepType

from ..verification_screen import VerificationScreen


def _check_is_every_field_set(verification_screen):
    """
    Asserts whether all fields are set of the given verification_screen.
    
    Parameters
    ----------
    verification_screen : ``VerificationScreen``
        The guild verification_screen instance to check.
    """
    vampytest.assert_instance(verification_screen, VerificationScreen)
    vampytest.assert_instance(verification_screen.edited_at, DateTime, nullable = True)
    vampytest.assert_instance(verification_screen.description, str, nullable = True)
    vampytest.assert_instance(verification_screen.steps, tuple, nullable = True)



def test__DiscoveryCategory__new__0():
    """
    Tests whether ``VerificationScreen.__new__`` works as intended.
    
    Case: No fields given.
    """
    verification_screen = VerificationScreen()
    _check_is_every_field_set(verification_screen)


def test__DiscoveryCategory__new__1():
    """
    Tests whether ``VerificationScreen.__new__`` works as intended.
    
    Case: All fields given.
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
    _check_is_every_field_set(verification_screen)
    
    vampytest.assert_eq(verification_screen.edited_at, edited_at)
    vampytest.assert_eq(verification_screen.description, description)
    vampytest.assert_eq(verification_screen.steps, tuple(steps))
