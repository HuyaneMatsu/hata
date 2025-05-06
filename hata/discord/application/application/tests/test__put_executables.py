import vampytest

from ...application_executable import ApplicationExecutable

from ..fields import put_executables


def test__put_executables():
    """
    Tests whether ``put_executables`` works as intended.
    
    Case: include internals.
    """
    application_executable = ApplicationExecutable(name = 'Red')
    
    for input_value, defaults, expected_output in (
        (None, True, {'executables': []}),
        (
            [application_executable],
            True,
            {'executables': [application_executable.to_data(defaults = True)]}
        ),
    ):
        data = put_executables(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
