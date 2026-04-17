import vampytest

from ...application_command import ApplicationCommand

from ..fields import validate_application_command_id


def test__validate_application_command_id__0():
    """
    Tests whether `validate_application_command_id` works as intended.
    
    Case: passing.
    """
    application_command_id = 202302210023
    
    application_command = ApplicationCommand('aa')
    application_command.id = application_command_id
    
    for input_value, expected_output in (
        (application_command_id, application_command_id),
        (str(application_command_id), application_command_id),
        (application_command, application_command_id),
    ):
        output = validate_application_command_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_application_command_id__1():
    """
    Tests whether `validate_application_command_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '-1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_application_command_id(input_value)


def test__validate_application_command_id__2():
    """
    Tests whether `validate_application_command_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_application_command_id(input_value)
