import vampytest

from ....permission import Permission

from ..fields import validate_application_permissions


def test__validate_application_permissions__0():
    """
    Tests whether `validate_application_permissions` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, Permission(1)),
        (Permission(1), Permission(1)),
    ):
        output = validate_application_permissions(input_value)
        vampytest.assert_instance(output, Permission)
        vampytest.assert_eq(output, expected_output)


def test__validate_application_permissions__1():
    """
    Tests whether `validate_application_permissions` works as intended.
    
    Case: type error
    """
    for input_value in (
        'a',
    ):
        with vampytest.assert_raises(TypeError):
            validate_application_permissions(input_value)
