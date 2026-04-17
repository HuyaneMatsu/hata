import vampytest

from ..constants import EXPIRE_GRACE_PERIOD_DEFAULT
from ..fields import validate_expire_grace_period


def test__validate_expire_grace_period__0():
    """
    Tests whether ``validate_expire_grace_period`` works as intended.
    
    Case: passing.
    """
    for input_parameter, expected_output in (
        (EXPIRE_GRACE_PERIOD_DEFAULT, EXPIRE_GRACE_PERIOD_DEFAULT),
    ):
        output = validate_expire_grace_period(input_parameter)
        vampytest.assert_eq(output, expected_output)


def test__validate_expire_grace_period__1():
    """
    Tests whether ``validate_expire_grace_period`` works as intended.
    
    Case: `ValueError`.
    """
    for input_parameter in (
        -2,
    ):
        with vampytest.assert_raises(ValueError):
            validate_expire_grace_period(input_parameter)


def test__validate_expire_grace_period__2():
    """
    Tests whether ``validate_expire_grace_period`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        '',
    ):
        with vampytest.assert_raises(TypeError):
            validate_expire_grace_period(input_parameter)
