from types import FunctionType

import vampytest

from ..conversion import _create_default_putter


def test__create_default_putter():
    """
    Tests whether ``_create_default_putter`` works as intended.
    """
    serializer_key = 'koishi'
    
    def serializer_optional(value):
        if value is not None:
            yield value
    
    def serializer_required(value):
        return value
    
    serializer_putter = _create_default_putter(serializer_key, serializer_optional, serializer_required)
    vampytest.assert_instance(serializer_putter, FunctionType)
    
    output = serializer_putter({}, False, None)
    vampytest.assert_eq(output, {})
    
    output = serializer_putter({}, True, None)
    vampytest.assert_eq(output, {'koishi': None})
    
    output = serializer_putter({}, False, 'hey')
    vampytest.assert_eq(output, {'koishi': 'hey'})
    
    output = serializer_putter({}, True, 'hey')
    vampytest.assert_eq(output, {'koishi': 'hey'})
