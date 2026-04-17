import vampytest

from ..conversion import ConversionMeta


def test__ConversionMeta__new():
    """
    Tests whether ``ConversionMeta.__new__`` works as intended.
    """
    class conversion_type(metaclass = ConversionMeta, instance = False):
        __slots__ = ('mister',)
        
        def __new__(cls, instance_attributes):
            mister = instance_attributes.pop('mister')
            
            self = object.__new__(cls)
            self.mister = mister
            return self
    
    vampytest.assert_instance(conversion_type, ConversionMeta)
    
    class instance(conversion_type):
        mister = 'hey'
    
    vampytest.assert_instance(instance, conversion_type)
    vampytest.assert_eq(instance.mister, 'hey')
