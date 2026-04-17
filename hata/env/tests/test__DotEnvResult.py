from types import FunctionType

import vampytest

from ..loading import DotEnvResult
from ..parsing import ParserFailureInfo


def _assert_fields_set(dot_env_result):
    """
    Asserts whether every fields are set of the given dot env result.
    
    Parameters
    ----------
    dot_env_result : ``DotEnvResult``
    """
    vampytest.assert_instance(dot_env_result, DotEnvResult)
    vampytest.assert_instance(dot_env_result.file_path, str, nullable = True)
    vampytest.assert_instance(dot_env_result.parser_failure_info, ParserFailureInfo)
    vampytest.assert_instance(dot_env_result.variables, dict)


def test__DotEnvResult__new():
    """
    Tests whether ``DotEnvResult.__new__`` works as intended.
    """
    variables = {'a': 'b'}
    parser_failure_info = ParserFailureInfo(6, '12', 2, 1)
    file_path = 'test_path'
    
    dot_env_result = DotEnvResult(variables, parser_failure_info, file_path)
    _assert_fields_set(dot_env_result)
    
    vampytest.assert_eq(dot_env_result.variables, variables)
    vampytest.assert_eq(dot_env_result.parser_failure_info, parser_failure_info)
    vampytest.assert_eq(dot_env_result.file_path, file_path)


def test__DotEnvResult__repr():
    """
    Tests whether ``DotEnvResult.__repr__`` works as intended.
    """
    variables = {'a': 'b'}
    parser_failure_info = ParserFailureInfo(6, '12', 2, 1)
    file_path = 'test_path'
    
    dot_env_result = DotEnvResult(variables, parser_failure_info, file_path)
    vampytest.assert_instance(repr(dot_env_result), str)


def test__DotEnvResult__insert_to_environmental_variables():
    """
    Tests whether ``DotEnvResult.insert_to_environmental_variables`` works as intended.
    """
    environmental_variables = {
        'Komeiji': 'Koishi',
    }
    
    environmental_variables_binary = {key.encode(): value.encode() for key, value in environmental_variables.items()}
    
    input_variables = {
        'Komeiji': 'Satori',
        'Chen': None,
        'Yakumo': 'Yukari',
    }
    
    expected_environmental_variables = {
        'Komeiji': 'Koishi',
        'Chen': '',
        'Yakumo': 'Yukari',
    }
    
    expected_environmental_variables_binary = {
        key.encode(): value.encode() for key, value in expected_environmental_variables.items()
    }
    
    dot_env_result = DotEnvResult(input_variables, None, None)
    
    
    insert_variables = type(dot_env_result).insert_to_environmental_variables
    
    mocked = vampytest.mock_globals(
        insert_variables,
        values = {
            'environmental_variables': environmental_variables,
            'environmental_variables_binary': environmental_variables_binary,
        },
    )
    
    output = mocked(dot_env_result)
    
    vampytest.assert_is(output, dot_env_result)
    
    vampytest.assert_eq(environmental_variables, expected_environmental_variables)
    vampytest.assert_eq(environmental_variables_binary, expected_environmental_variables_binary)



def test__DotEnvResult__insert_to_environmental_variables__no_binary_supported():
    """
    Tests whether ``DotEnvResult.insert_to_environmental_variables`` works as intended.
    """
    environmental_variables = {
        'Komeiji': 'Koishi',
    }
    
    input_variables = {
        'Komeiji': 'Satori',
        'Chen': None,
        'Yakumo': 'Yukari',
    }
    
    expected_environmental_variables = {
        'Komeiji': 'Koishi',
        'Chen': '',
        'Yakumo': 'Yukari',
    }
    
    dot_env_result = DotEnvResult(input_variables, None, None)
    
    
    insert_variables = type(dot_env_result).insert_to_environmental_variables
    
    mocked = vampytest.mock_globals(
        insert_variables,
        values = {
            'environmental_variables': environmental_variables,
            'environmental_variables_binary': None,
        },
    )
    
    output = mocked(dot_env_result)
    
    vampytest.assert_is(output, dot_env_result)
    
    vampytest.assert_eq(environmental_variables, expected_environmental_variables)


def test__DotEnvResult__raise_if_failed__0():
    """
    Tests whether ``DotEnvResult.raise_if_failed`` works as intended.
    
    Case: Raising.
    """
    variables = {'a': 'b'}
    parser_failure_info = ParserFailureInfo(6, '12', 2, 1)
    file_path = 'test_path'
    
    dot_env_result = DotEnvResult(variables, parser_failure_info, file_path)
    
    with vampytest.assert_raises(SyntaxError):
        dot_env_result.raise_if_failed()


def test__DotEnvResult__raise_if_failed__1():
    """
    Tests whether ``DotEnvResult.raise_if_failed`` works as intended.
    
    Case: Good.
    """
    variables = {'a': 'b'}
    parser_failure_info = None
    file_path = 'test_path'
    
    dot_env_result = DotEnvResult(variables, parser_failure_info, file_path)
    
    output = dot_env_result.raise_if_failed()
    vampytest.assert_is(output, dot_env_result)
