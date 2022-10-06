import vampytest

from ....permission import Permission

from ..deny import validate_deny


def test__validate_deny__0():
    """
    Tests whether ``validate_deny`` works as intended.
    
    Case: passing.
    """
    deny = Permission(11111)
    
    for input_value, expected_output in (
        (deny, deny),
        (int(deny), deny),
        (None, Permission()),
    ):
        output = validate_deny(input_value)
        vampytest.assert_instance(output, Permission)
        vampytest.assert_eq(output, expected_output)


def test__validate_deny__1():
    """
    Tests whether ``validate_deny`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.5,
    ):
        with vampytest.assert_raises(TypeError):
            validate_deny(input_value)
