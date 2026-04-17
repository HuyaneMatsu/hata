import vampytest

from ..preinstance import Preinstance
from ..preinstanced_meta import PreinstancedMeta


def test__PreinstancedMeta__new():
    """
    Tests whether ``PreinstancedMeta.__new__`` works as intended.
    """
    name_default = 'nue'
    value_type = int
    
    class preinstance_type(metaclass = PreinstancedMeta, name_default = name_default, value_type = value_type):
        koishi = Preinstance(12, 'koi')
        satori = Preinstance(13, 'sato')
        
        __slots__ = ('name', 'value')
        
        def __new__(cls, value, name = None):
            if name is None:
                name = cls.NAME_DEFAULT
            
            self = object.__new__(cls)
            self.value = value
            self.name = name
            return self
    
    
    vampytest.assert_instance(preinstance_type, PreinstancedMeta)
    
    vampytest.assert_instance(preinstance_type.koishi, preinstance_type)
    vampytest.assert_eq(preinstance_type.koishi.value, 12)
    vampytest.assert_eq(preinstance_type.koishi.name, 'koi')
    
    vampytest.assert_instance(preinstance_type.satori, preinstance_type)
    vampytest.assert_eq(preinstance_type.satori.value, 13)
    vampytest.assert_eq(preinstance_type.satori.name, 'sato')
    
    vampytest.assert_eq(
        preinstance_type.INSTANCES,
        {
            preinstance_type.koishi.value: preinstance_type.koishi,
            preinstance_type.satori.value: preinstance_type.satori,
        },
    )
    
    vampytest.assert_eq(preinstance_type.VALUE_TYPE, value_type)
    vampytest.assert_eq(preinstance_type.NAME_DEFAULT, name_default)
    vampytest.assert_eq(preinstance_type.VALUE_DEFAULT, 0)
    
    # Test __call__ as well
    output = preinstance_type(12)
    vampytest.assert_instance(output, preinstance_type)
    vampytest.assert_is(output, preinstance_type.koishi)
    
    output = preinstance_type(None)
    vampytest.assert_instance(output, preinstance_type)
    vampytest.assert_eq(output.value, 0)
    vampytest.assert_eq(output.name, name_default)
