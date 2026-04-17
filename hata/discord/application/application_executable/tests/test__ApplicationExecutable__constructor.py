import vampytest

from ..application_executable import ApplicationExecutable
from ..preinstanced import OperationSystem


def _assert_fields_set(application_executable):
    """
    Asserts whether every attributes are set of the given application executable.
    
    Parameters
    ----------
    application_executable : ``ApplicationExecutable``
    """
    vampytest.assert_instance(application_executable, ApplicationExecutable)
    vampytest.assert_instance(application_executable.launcher, bool)
    vampytest.assert_instance(application_executable.name, str)
    vampytest.assert_instance(application_executable.os, OperationSystem)
    vampytest.assert_instance(application_executable.parameters, str, nullable = True)



def test__ApplicationExecutable__new__0():
    """
    Tests whether ``ApplicationExecutable.__new__`` works as intended.
    
    Case: No parameters.
    """
    application_executable = ApplicationExecutable()
    _assert_fields_set(application_executable)


def test__ApplicationExecutable__new__1():
    """
    Tests whether ``ApplicationExecutable.__new__`` works as intended.
    
    Case: Give all parameters.
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
    
    _assert_fields_set(application_executable)
    vampytest.assert_eq(application_executable.launcher, launcher)
    vampytest.assert_eq(application_executable.name, name)
    vampytest.assert_is(application_executable.os, os)
    vampytest.assert_eq(application_executable.parameters, parameters)
