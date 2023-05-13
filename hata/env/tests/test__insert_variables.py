import vampytest

from types import FunctionType

from ..loading import insert_variables


def test__insert_variables():
    """
    Tests whether ``insert_variables`` works as intended.
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
    
    insert_variables_copy = FunctionType(
        insert_variables.__code__,
        {
            **insert_variables.__globals__,
            'environmental_variables': environmental_variables,
            'environmental_variables_binary': environmental_variables_binary,
        },
        insert_variables.__name__,
        insert_variables.__defaults__,
        insert_variables.__closure__,
    )
    
    insert_variables_copy(input_variables)
    
    vampytest.assert_eq(environmental_variables, expected_environmental_variables)
    vampytest.assert_eq(environmental_variables_binary, expected_environmental_variables_binary)
