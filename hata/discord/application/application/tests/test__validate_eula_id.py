import vampytest

from ...eula import EULA

from ..fields import validate_eula_id


def test__validate_eula_id__0():
    """
    Tests whether `validate_eula_id` works as intended.
    
    Case: passing.
    """
    eula_id = 202211270008
    
    for input_value, expected_output in (
        (eula_id, eula_id),
        (str(eula_id), eula_id),
        (EULA.precreate(eula_id), eula_id),
    ):
        output = validate_eula_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_eula_id__1():
    """
    Tests whether `validate_eula_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_eula_id(input_value)


def test__validate_eula_id__2():
    """
    Tests whether `validate_eula_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_eula_id(input_value)
