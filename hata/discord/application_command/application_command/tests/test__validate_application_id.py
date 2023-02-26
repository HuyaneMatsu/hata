import vampytest

from ....application import Application

from ..fields import validate_application_id


def test__validate_application_id__0():
    """
    Tests whether `validate_application_id` works as intended.
    
    Case: passing.
    """
    application_id = 202302260002
    
    for input_value, expected_output in (
        (None, 0),
        (application_id, application_id),
        (Application.precreate(application_id), application_id),
        (str(application_id), application_id)
    ):
        output = validate_application_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_application_id__1():
    """
    Tests whether `validate_application_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_application_id(input_value)


def test__validate_application_id__2():
    """
    Tests whether `validate_application_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_application_id(input_value)
