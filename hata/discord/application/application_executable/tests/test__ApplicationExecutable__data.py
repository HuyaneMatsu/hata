import vampytest

from ..application_executable import ApplicationExecutable
from ..preinstanced import OperationSystem

from .test__ApplicationExecutable__constructor import _assert_fields_set


def test__ApplicationExecutable__from_data():
    """
    Tests whether ``ApplicationExecutable.from_data`` works as intended.
    """
    launcher = True
    name = 'WARNING'
    os = OperationSystem.linux
    parameters = 'run'
    
    data = {
        'is_launcher': launcher,
        'name': name,
        'os': os.value,
        'parameters': parameters,
    }
    
    application_executable = ApplicationExecutable.from_data(data)
    _assert_fields_set(application_executable)
    
    vampytest.assert_eq(application_executable.launcher, launcher)
    vampytest.assert_eq(application_executable.name, name)
    vampytest.assert_is(application_executable.os, os)
    vampytest.assert_eq(application_executable.parameters, parameters)


def test__ApplicationExecutable__to_data():
    """
    Tests whether ``ApplicationExecutable.to_data`` works as intended.
    
    Case: Include defaults.
    """
    launcher = True
    name = 'WARNING'
    os = OperationSystem.linux
    parameters = 'run'
    
    application_executable = ApplicationExecutable(
        launcher = launcher,
        name = name,
        os = os,
        parameters = parameters,
    )
    
    expected_output = {
        'is_launcher': launcher,
        'name': name,
        'os': os.value,
        'parameters': parameters,
    }
    
    vampytest.assert_eq(application_executable.to_data(defaults = True), expected_output)
