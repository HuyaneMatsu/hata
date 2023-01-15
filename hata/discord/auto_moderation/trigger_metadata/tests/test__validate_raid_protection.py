import vampytest

from ..fields import validate_raid_protection


def test__validate_raid_protection__0():
    """
    Tests whether `validate_raid_protection` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_raid_protection(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_raid_protection__1():
    """
    Tests whether `validate_raid_protection` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_raid_protection(input_value)
