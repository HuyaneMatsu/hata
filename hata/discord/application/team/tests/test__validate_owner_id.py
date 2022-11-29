import vampytest

from ..fields import validate_owner_id


def test__validate_owner_id__0():
    """
    Tests whether `validate_owner_id` works as intended.
    
    Case: passing.
    """
    owner_id = 202211230019
    
    for input_value, expected_output in (
        (owner_id, owner_id),
        (str(owner_id), owner_id)
    ):
        output = validate_owner_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_owner_id__1():
    """
    Tests whether `validate_owner_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_owner_id(input_value)


def test__validate_owner_id__2():
    """
    Tests whether `validate_owner_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_owner_id(input_value)
