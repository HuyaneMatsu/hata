import vampytest

from ..precreate_helpers import process_precreate_parameters


def test__process_precreate_parameters__0():
    """
    Tests whether ``process_precreate_parameters`` works as intended.
    
    Case: No extra.
    """
    keyword_parameters = {'neko': 'love'}
    
    field_processors = {
        'neko': ('neko-chan', lambda x: f'{x}-{x}'),
    }
    
    processed = []
    extra = process_precreate_parameters(keyword_parameters, field_processors, processed)
    
    vampytest.assert_is(extra, None)
    vampytest.assert_eq(processed, [('neko-chan', 'love-love')])


def test__process_precreate_parameters__extra():
    """
    Tests whether ``process_precreate_parameters`` works as intended.
    
    Case: Extra.
    """
    keyword_parameters = {'neko': 'love'}
    
    field_processors = {}
    
    processed = []
    extra = process_precreate_parameters(keyword_parameters, field_processors, processed)
    
    vampytest.assert_eq(extra, {'neko': 'love'})
    vampytest.assert_eq(processed, [])
