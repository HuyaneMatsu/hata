import vampytest

from .. import SetupFunction


def test__SetupFunction__call():
    """
    Tests whether ``SetupFunction.__call__`` works as intended.
    """
    extension_name = 'hell'
    
    setup_function_called = False
    received_client = None
    received_positional_parameters = None
    received_keyword_parameters = None
    
    def setup_function(client, *positional_parameters, **keyword_parameters):
        nonlocal setup_function_called
        nonlocal received_client
        nonlocal received_positional_parameters
        nonlocal received_keyword_parameters
        
        setup_function_called = True
        received_client = client
        received_positional_parameters = positional_parameters
        received_keyword_parameters = keyword_parameters
    
    required_parameters = ('shrimp',)
    optional_parameters = ('fry',)
    
    setup_function = SetupFunction(extension_name, setup_function, required_parameters, optional_parameters)
    
    input_keyword_parameters = {
        'shrimp': 'eaten',
        'fry': 'fried shrimp',
        'potato': 'also fried',
    }
    
    test_client = object()
    
    expected_positional_parameters = ('eaten',)
    expected_keyword_parameters = {'fry': 'fried shrimp'}
    
    setup_function(test_client, input_keyword_parameters)
    
    vampytest.assert_eq(setup_function_called, True)
    vampytest.assert_is(received_client, test_client)
    vampytest.assert_eq(received_positional_parameters, expected_positional_parameters)
    vampytest.assert_eq(received_keyword_parameters, expected_keyword_parameters)
