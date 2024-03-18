from types import FunctionType

import vampytest

from ..constants import CONVERSION_KIND_FIELD, CONVERSION_KIND_NONE
from ..conversion import Conversion


def _assert_fields_set(conversion):
    """
    Asserts whether every fields are set of the given conversion.
    
    Parameters
    ----------
    conversion : ``Conversion``
        The conversion to check
    """
    vampytest.assert_instance(conversion, Conversion)
    vampytest.assert_instance(conversion.name_aliases, tuple, nullable = True)
    vampytest.assert_instance(conversion.expected_types_messages, str)
    vampytest.assert_instance(conversion.set_identifier, FunctionType, nullable = True)
    vampytest.assert_instance(conversion.serializer_key, str, nullable = True)
    vampytest.assert_instance(conversion.kind, int)
    vampytest.assert_instance(conversion.set_merger, FunctionType, nullable = True)
    vampytest.assert_instance(conversion.name, str)
    vampytest.assert_instance(conversion.output_conversion, type(conversion), nullable = True)
    vampytest.assert_instance(conversion.serializer_optional, FunctionType, nullable = True)
    vampytest.assert_instance(conversion.serializer_required, FunctionType, nullable = True)
    vampytest.assert_instance(conversion.set_validator, FunctionType, nullable = True)
    vampytest.assert_instance(conversion.get_default, object)
    vampytest.assert_instance(conversion.get_processor, FunctionType, nullable = True)
    vampytest.assert_instance(conversion.serializer_putter, FunctionType, nullable = True)
    vampytest.assert_instance(conversion.sort_priority, int)
    vampytest.assert_instance(conversion.set_type, type, nullable = True)


def test__Conversion__new():
    """
    Tests whether ``Conversion.__new__`` works as intended.
    """
    name_aliases = ('hey', 'mister')
    expected_types_messages = '`str`'
    
    def set_identifier(value):
        yield value
    
    serializer_key = 'koishi'
    kind = CONVERSION_KIND_FIELD
    
    def set_merger(old_value, new_value):
        return old_value + new_value
    
    name = 'satori'
    
    output_conversion = None
    
    def serializer_optional(value):
        yield value
    
    def serializer_required(value):
        return value
    
    def set_validator(value):
        yield value
    
    get_default = 14
    
    def get_processor(value):
        return value
    
    def serializer_putter(data, required, value):
        return data
    
    sort_priority = 10
    
    set_type = int
    
    def set_type_processor(value):
        return value
    
    def set_listing_identifier(value):
        yield value
    
    
    instance_attributes = {
        'name_aliases': name_aliases,
        'expected_types_messages': expected_types_messages,
        'set_identifier': set_identifier,
        'serializer_key': serializer_key,
        'kind': kind,
        'set_merger': set_merger,
        'name': name,
        'output_conversion': output_conversion,
        'serializer_optional': serializer_optional,
        'serializer_required': serializer_required,
        'set_validator': set_validator,
        'get_default': get_default,
        'get_processor': get_processor,
        'serializer_putter': serializer_putter,
        'sort_priority': sort_priority,
        'set_type': set_type,
        'set_type_processor': set_type_processor,
        'set_listing_identifier': set_listing_identifier,
    }
    
    conversion = Conversion(instance_attributes)
    _assert_fields_set(conversion)
    
    vampytest.assert_eq(conversion.name_aliases, name_aliases)
    vampytest.assert_eq(conversion.expected_types_messages, expected_types_messages)
    vampytest.assert_is(conversion.set_identifier, set_identifier)
    vampytest.assert_eq(conversion.serializer_key, serializer_key)
    vampytest.assert_eq(conversion.kind, kind)
    vampytest.assert_is(conversion.set_merger, set_merger)
    vampytest.assert_eq(conversion.name, name)
    vampytest.assert_is(conversion.output_conversion, output_conversion)
    vampytest.assert_is(conversion.serializer_optional, serializer_optional)
    vampytest.assert_is(conversion.serializer_required, serializer_required)
    vampytest.assert_is(conversion.set_validator, set_validator)
    vampytest.assert_eq(conversion.get_default, get_default)
    vampytest.assert_is(conversion.get_processor, get_processor)
    vampytest.assert_is(conversion.serializer_putter, serializer_putter)
    vampytest.assert_eq(conversion.sort_priority, sort_priority)
    vampytest.assert_is(conversion.set_type, set_type)
    vampytest.assert_is(conversion.set_type_processor, set_type_processor)
    vampytest.assert_is(conversion.set_listing_identifier, set_listing_identifier)


def test__Conversion__new__serializer_putter__none():
    """
    Tests whether ``Conversion.__new__`` works as intended.
    
    Case: `serializer_putter` becomes `None`.
    """
    name_aliases = None
    expected_types_messages = ''
    set_identifier = None
    serializer_key = 'koishi'
    kind = CONVERSION_KIND_FIELD
    set_merger = None
    name = 'satori'
    output_conversion = None
    serializer_optional = None
    serializer_required = None
    set_validator = None
    get_default = None
    get_processor = None
    serializer_putter = None
    sort_priority = 0
    set_type = None
    set_type_processor = None
    set_listing_identifier = None,
    
    
    instance_attributes = {
        'name_aliases': name_aliases,
        'expected_types_messages': expected_types_messages,
        'set_identifier': set_identifier,
        'serializer_key': serializer_key,
        'kind': kind,
        'set_merger': set_merger,
        'name': name,
        'output_conversion': output_conversion,
        'serializer_optional': serializer_optional,
        'serializer_required': serializer_required,
        'set_validator': set_validator,
        'get_default': get_default,
        'get_processor': get_processor,
        'serializer_putter': serializer_putter,
        'sort_priority': sort_priority,
        'set_type': set_type,
        'set_type_processor': set_type_processor,
        'set_listing_identifier': set_listing_identifier,
    }
    
    conversion = Conversion(instance_attributes)
    _assert_fields_set(conversion)
    
    vampytest.assert_is(conversion.serializer_putter, None)


def test__Conversion__new__serializer_putter__default():
    """
    Tests whether ``Conversion.__new__`` works as intended.
    
    Case: `serializer_putter` is defaulted.
    """
    name_aliases = None
    expected_types_messages = ''
    set_identifier = None
    serializer_key = 'koishi'
    kind = CONVERSION_KIND_FIELD
    set_merger = None
    name = 'satori'
    output_conversion = None
    
    def serializer_optional(value):
        yield value
    
    def serializer_required(value):
        return value
    
    set_validator = None
    get_default = None
    get_processor = None
    serializer_putter = None
    sort_priority = 0
    set_type = None
    set_type_processor = None
    set_listing_identifier = None
    
    
    instance_attributes = {
        'name_aliases': name_aliases,
        'expected_types_messages': expected_types_messages,
        'set_identifier': set_identifier,
        'serializer_key': serializer_key,
        'kind': kind,
        'set_merger': set_merger,
        'name': name,
        'output_conversion': output_conversion,
        'serializer_optional': serializer_optional,
        'serializer_required': serializer_required,
        'set_validator': set_validator,
        'get_default': get_default,
        'get_processor': get_processor,
        'serializer_putter': serializer_putter,
        'sort_priority': sort_priority,
        'set_type': set_type,
        'set_type_processor': set_type_processor,
        'set_listing_identifier': set_listing_identifier,
    }
    
    conversion = Conversion(instance_attributes)
    _assert_fields_set(conversion)
    
    vampytest.assert_is_not(conversion.serializer_putter, None)


def _iter_options__iter_names():
    instance_attributes = {
        'name_aliases': None,
        'expected_types_messages': '',
        'set_identifier': None,
        'serializer_key': None,
        'kind': CONVERSION_KIND_NONE,
        'set_merger': None,
        'name': '',
        'output_conversion': None,
        'serializer_optional': None,
        'serializer_required': None,
        'set_validator': None,
        'get_default': None,
        'get_processor': None,
        'sort_priority': 0,
        'set_type': None,
        'set_type_processor': None,
        'set_listing_identifier': None,
    }
    
    yield (
        Conversion({**instance_attributes, 'name': 'koishi'}),
        ['koishi', ],
    )
    yield (
        Conversion({**instance_attributes, 'name': 'koishi', 'name_aliases': ('satori', 'orin')}),
        ['koishi', 'satori', 'orin'],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_names()).returning_last())
def test__Conversion__iter_names(conversion):
    """
    Tests whether ``Conversion.iter_names`` works as intended.
    
    Parameters
    ----------
    conversion : ``Conversion``
        The conversion to test.
    
    Returns
    -------
    output : `list<str>`
    """
    output = [*conversion.iter_names()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output


def test__Conversion__repr():
    """
    Tests whether ``Conversion.__repr__`` works as intended.
    """
    name_aliases = ('hey', 'mister')
    expected_types_messages = '`str`'
    
    def set_identifier(value):
        yield value
    
    serializer_key = 'koishi'
    kind = CONVERSION_KIND_FIELD
    
    def set_merger(old_value, new_value):
        return old_value + new_value
    
    name = 'satori'
    
    output_conversion = None
    
    def serializer_optional(value):
        yield value
    
    def serializer_required(value):
        return value
    
    def set_validator(value):
        yield value
    
    get_default = 14
    
    def get_processor(value):
        return value
    
    sort_priority = 2
    set_type = int
    
    def set_type_processor(value):
        return value
    
    def set_listing_identifier(value):
        yield value
    
          
    instance_attributes = {
        'name_aliases': name_aliases,
        'expected_types_messages': expected_types_messages,
        'set_identifier': set_identifier,
        'serializer_key': serializer_key,
        'kind': kind,
        'set_merger': set_merger,
        'name': name,
        'output_conversion': output_conversion,
        'serializer_optional': serializer_optional,
        'serializer_required': serializer_required,
        'set_validator': set_validator,
        'get_default': get_default,
        'get_processor': get_processor,
        'sort_priority': sort_priority,
        'set_type': set_type,
        'set_type_processor': set_type_processor,
        'set_listing_identifier': set_listing_identifier,
    }
    
    conversion = Conversion(instance_attributes)
    
    output = repr(conversion)
    
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in('name', output)
    vampytest.assert_in(repr(name), output)
