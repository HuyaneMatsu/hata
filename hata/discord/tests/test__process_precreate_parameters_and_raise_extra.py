import vampytest

from ..precreate_helpers import process_precreate_parameters_and_raise_extra


def test__process_precreate_parameters_and_raise_extra__0():
    """
    Tests whether ``process_precreate_parameters_and_raise_extra`` works as intended.
    
    Case: No extra.
    """
    keyword_parameters = {'neko': 'love'}
    
    field_processors = {
        'neko': ('neko-chan', lambda x: f'{x}-{x}'),
    }
    
    processed = process_precreate_parameters_and_raise_extra(keyword_parameters, field_processors)
    vampytest.assert_eq(processed, [('neko-chan', 'love-love')])


def test__process_precreate_parameters_and_raise_extra__extra():
    """
    Tests whether ``process_precreate_parameters_and_raise_extra`` works as intended.
    
    Case: Extra.
    """
    keyword_parameters = {'neko': 'love'}
    
    field_processors = {}
    
    with vampytest.assert_raises(TypeError):
        process_precreate_parameters_and_raise_extra(keyword_parameters, field_processors)
