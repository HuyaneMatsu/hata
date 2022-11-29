import vampytest

from ..application_executable import ApplicationExecutable
from ..preinstanced import OperationSystem


def test__ApplicationExecutable__repr():
    """
    Tests whether ``ApplicationExecutable.__repr__`` works as intended.
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
    
    vampytest.assert_instance(repr(application_executable), str)


def test__ApplicationExecutable__hash():
    """
    Tests whether ``ApplicationExecutable.__hash__`` works as intended.
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
    
    vampytest.assert_instance(hash(application_executable), int)


def test__ApplicationExecutable__eq():
    """
    Tests whether ``ApplicationExecutable.__eq__`` works as intended.
    """
    launcher = True
    name = 'WARNING'
    os = OperationSystem.linux
    parameters = 'run'
    
    keyword_parameters = {
        'launcher': launcher,
        'name': name,
        'os': os,
        'parameters': parameters,
    }
    
    application_executable = ApplicationExecutable(**keyword_parameters)
    vampytest.assert_eq(application_executable, application_executable)
    vampytest.assert_ne(application_executable, object())
    
    for field_name, field_value in (
        ('launcher', False),
        ('name', 'okuu'),
        ('os', OperationSystem.none),
        ('parameters', 'walk')
    ):
        test_application_executable = ApplicationExecutable(
            **{**keyword_parameters, field_name: field_value}
        )
        vampytest.assert_ne(application_executable, test_application_executable)


def test__ApplicationExecutable__sort():
    """
    Tests whether ``ApplicationExecutable`` sorting works as intended.
    """
    application_executable_0 = ApplicationExecutable(
        launcher = True,
        name = 'WARNING',
        os = OperationSystem.linux,
        parameters = 'run',
    )
    
    application_executable_1 = ApplicationExecutable(
        launcher = False,
        name = 'WARNING',
        os = OperationSystem.linux,
        parameters = 'run',
    )
    
    application_executable_2 = ApplicationExecutable(
        launcher = True,
        name = 'LIFE IS A FLOWER',
        os = OperationSystem.linux,
        parameters = 'run',
    )
    
    application_executable_3 = ApplicationExecutable(
        launcher = True,
        name = 'WARNING',
        os = OperationSystem.none,
        parameters = 'run',
    )
    
    application_executable_4 = ApplicationExecutable(
        launcher = True,
        name = 'WARNING',
        os = OperationSystem.linux,
        parameters = None,
    )
    
    application_executable_5 = ApplicationExecutable(
        launcher = True,
        name = 'WARNING',
        os = OperationSystem.linux,
        parameters = 'sit',
    )
    
    vampytest.assert_eq(
        sorted([
            application_executable_0,
            application_executable_1,
            application_executable_2,
            application_executable_3,
            application_executable_4,
            application_executable_5,
        ]),
        [
            application_executable_2,
            application_executable_3,
            application_executable_1,
            application_executable_4,
            application_executable_0,
            application_executable_5,
        ]
    )
