import vampytest

from ..application_executable import ApplicationExecutable
from ..preinstanced import OperationSystem

from .test__ApplicationExecutable__constructor import _assert_fields_set


def test__ApplicationExecutable__copy():
    """
    Tests whether ``ApplicationExecutable.copy`` works as intended.
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
    
    copy = application_executable.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(application_executable, copy)
    vampytest.assert_is_not(application_executable, copy)


def test__ApplicationExecutable__copy_with__0():
    """
    Tests whether ``ApplicationExecutable.copy`` works as intended.
    
    Case: No parameters
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
    
    copy = application_executable.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_eq(application_executable, copy)
    vampytest.assert_is_not(application_executable, copy)


def test__ApplicationExecutable__copy_with__1():
    """
    Tests whether ``ApplicationExecutable.copy`` works as intended.
    
    Case: No parameters
    """
    old_launcher = True
    new_launcher = False
    old_name = 'WARNING'
    new_name = 'Okuu'
    old_os = OperationSystem.linux
    new_os = OperationSystem.none
    old_parameters = 'run'
    new_parameters = 'walk'
    
    application_executable = ApplicationExecutable(
        launcher = old_launcher,
        name = old_name,
        os = old_os,
        parameters = old_parameters,
    )
    
    copy = application_executable.copy_with(
        launcher = new_launcher,
        name = new_name,
        os = new_os,
        parameters = new_parameters,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(application_executable, copy)

    vampytest.assert_eq(copy.launcher, new_launcher)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_is(copy.os, new_os)
    vampytest.assert_eq(copy.parameters, new_parameters)
