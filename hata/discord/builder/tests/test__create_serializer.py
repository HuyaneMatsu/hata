from types import FunctionType

import vampytest

from ..builder_base import BuilderBase
from ..constants import CONVERSION_KIND_FIELD
from ..serialization import create_serializer
from ..serialization_configuration import SerializationConfiguration

from .helpers import _create_default_conversion


def test__create_serializer():
    """
    Tests whether ``create_serializer`` works as intended.
    """
    def serializer_optional(value):
        if value:
            yield value
    
    def serializer_required(value):
        return value
    
    
    def set_validator(value):
        if isinstance(value, bool):
            yield value
    
    
    conversion_0 = _create_default_conversion({
        'name': 'koishi',
        'kind': CONVERSION_KIND_FIELD,
        'serializer_key': 'koishi',
        'set_type': int,
        'serializer_optional': serializer_optional,
        'serializer_required': serializer_required,
    })
    conversion_1 = _create_default_conversion({
        'name': 'satori',
        'kind': CONVERSION_KIND_FIELD,
        'serializer_key': 'satori',
        'set_type': str,
        'serializer_optional': serializer_optional,
        'serializer_required': serializer_required,
    })
    conversion_2 = _create_default_conversion({
        'name': 'orin',
        'kind': CONVERSION_KIND_FIELD,
        'serializer_key': 'orin',
        'set_type': bool,
        'serializer_optional': serializer_optional,
        'serializer_required': serializer_required,
        'set_validator': set_validator,
    })
    
    
    class TestBuilder(BuilderBase):
        koishi = conversion_0
        satori = conversion_1
        orin = conversion_2
        
        __slots__ = ('fields',)
        
        def __new__(cls):
            self = object.__new__(cls)
            self.fields = {}
            return self
        
        
        def _store_field_value(self, conversion, value):
            self.fields[conversion] = value
        
        
        def _try_pull_field_value(self, conversion):
            try:
                yield self.fields[conversion]
            except KeyError:
                pass
        
        
        def _iter_fields(self):
            yield from self.fields.items()
        
        
        def _with_keyword_parameter_unknown(self, key, value):
            raise KeyError(key)
    
    
    serializer_configuration = SerializationConfiguration([TestBuilder.koishi, TestBuilder.orin], False)
    
    serializer = create_serializer(TestBuilder, serializer_configuration)
    vampytest.assert_instance(serializer, FunctionType)
    
    output = serializer((12, 'mister'), {'orin': True})
    vampytest.assert_eq(
        output,
        {
            'koishi': 12,
            'orin': True,
        },
    )
