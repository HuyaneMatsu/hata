import vampytest

from ...application_executable import ApplicationExecutable

from ..fields import validate_executables


def test__validate_executables__0():
    """
    Tests whether ``validate_executables`` works as intended.
    
    Case: passing.
    """
    application_executable = ApplicationExecutable(name = 'Red')
    
    for input_parameter, expected_output in (
        (None, None),
        ([], None),
        ([application_executable], (application_executable, ))
    ):
        output = validate_executables(input_parameter)
        vampytest.assert_eq(output, expected_output)


def test__validate_executables__1():
    """
    Tests whether ``validate_executables`` works as intended.
    """
    application_executable = ApplicationExecutable(name = 'Red')
    
    for input_value in (
        12.3,
        [32.1]
    ):
        with vampytest.assert_raises(TypeError):
            validate_executables(input_value)
