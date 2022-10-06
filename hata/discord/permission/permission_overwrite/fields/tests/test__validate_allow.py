import vampytest

from ....permission import Permission

from ..allow import validate_allow


def test__validate_allow__0():
    """
    Tests whether ``validate_allow`` works as intended.
    
    Case: passing.
    """
    allow = Permission(11111)
    
    for input_value, expected_output in (
        (allow, allow),
        (int(allow), allow),
        (None, Permission()),
    ):
        output = validate_allow(input_value)
        vampytest.assert_instance(output, Permission)
        vampytest.assert_eq(output, expected_output)


def test__validate_allow__1():
    """
    Tests whether ``validate_allow`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.5,
    ):
        with vampytest.assert_raises(TypeError):
            validate_allow(input_value)
