import vampytest
from ..loading import DotEnvResult, load_dot_env


def test__load_dot_env():
    """
    Tests whether ``load_dot_env`` works as intended.
    """
    content = 'a=b\nc=d'
    
    expected_variables = {
        'a': 'b',
        'c': 'd',
    }
    
    output = load_dot_env(content)
    
    vampytest.assert_instance(output, DotEnvResult)
    vampytest.assert_eq(output.variables, expected_variables)
