import vampytest

from ...application_executable import ApplicationExecutable

from ..fields import parse_executables


def test__parse_executables():
    """
    Tests whether ``parse_executables`` works as intended.
    """
    application_executable = ApplicationExecutable(name = 'Red')
    
    for input_data, expected_output in (
        ({}, None),
        ({'executables': None}, None),
        ({'executables': []}, None),
        (
            {'executables': [application_executable.to_data(defaults = True)]},
            (application_executable, )
        )
    ):
        output = parse_executables(input_data)
        
        vampytest.assert_eq(output, expected_output)
