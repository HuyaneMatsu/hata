import vampytest
from scarletio import is_generator_function

from ..builder_base import BuilderBase
from ..constants import CONVERSION_KIND_FIELD
from ..serialization_configuration import SerializationConfiguration

from .helpers import _create_default_conversion


def _assert_fields_set(builder):
    """
    Asserts whether every fields of the builder are set.
    
    Parameters
    ----------
    builder : ``BuilderBase``
        The builder to check
    """
    vampytest.assert_instance(builder, BuilderBase)


def test__BuilderBase__new():
    """
    Tests whether ``BuilderBase.__new__`` works as intended.
    """
    builder = BuilderBase()
    _assert_fields_set(builder)


def test__BuilderBase__eq__same_type():
    """
    Tests whether ``BuilderBase.__eq__`` works as intended.
    
    Case: Same type.
    """
    builder_0 = BuilderBase()
    builder_1 = BuilderBase()
    
    output = builder_0 == builder_1
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__BuilderBase__eq__different_type():
    """
    Tests whether ``BuilderBase.__eq__`` works as intended.
    
    Case : different type.
    """
    builder = BuilderBase()
    
    output = builder == object()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__BuilderBase__hash():
    """
    Tests whether ``BuilderBase.__hash__`` works as intended.
    """
    builder = BuilderBase()
    
    output = hash(builder)
    vampytest.assert_instance(output, int)


def test__BuilderBase__repr():
    """
    Tests whether ``BuilderBase.__repr__`` works as intended.
    """
    builder = BuilderBase()
    
    output = repr(builder)
    vampytest.assert_instance(output, str)


def test__BuilderBase__setter_none():
    """
    Tests whether ``BuilderBase._setter_none`` works as intended.
    """
    builder = BuilderBase()
    conversion = _create_default_conversion()
    
    output = builder._setter_none(conversion, None)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__BuilderBase__setter_field__no_merger():
    """
    Tests whether ``BuilderBase._setter_field`` works as intended.
    
    Case: No merger.
    """
    conversion = _create_default_conversion()
    store_called_field = False
    value = 1
    
    class TestBuilder(BuilderBase):
        def _store_field_value(self, input_conversion, input_value):
            nonlocal store_called_field
            nonlocal conversion
            nonlocal value
            vampytest.assert_is(conversion, input_conversion)
            vampytest.assert_eq(value, input_value)
            store_called_field = True
    
    
    builder = TestBuilder()
    output = builder._setter_field(conversion, value)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_true(store_called_field)


def test__BuilderBase__setter_field__with_merger():
    """
    Tests whether ``BuilderBase._setter_field`` works as intended.
    
    Case: with merger.
    """
    def set_merger(old_value, new_value):
        return old_value | new_value
    
    
    conversion = _create_default_conversion({
        'set_merger': set_merger,
    })
    store_called_field = False
    value = 1
    value_to_pull = 2
    
    
    class TestBuilder(BuilderBase):
        def _store_field_value(self, input_conversion, input_value):
            nonlocal store_called_field
            nonlocal conversion
            nonlocal value
            nonlocal value_to_pull
            nonlocal set_merger
            vampytest.assert_is(conversion, input_conversion)
            vampytest.assert_eq(set_merger(value, value_to_pull), input_value)
            store_called_field = True
        
        
        def _try_pull_field_value(self, input_conversion):
            nonlocal value_to_pull
            nonlocal conversion
            vampytest.assert_is(conversion, input_conversion)
            yield value_to_pull
    
    
    builder = TestBuilder()
    output = builder._setter_field(conversion, value)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_true(store_called_field)


def test__BuilderBase__setter_positional():
    """
    Tests whether ``BuilderBase._setter_positional`` works as intended.
    """
    with_positional_parameters_called = False
    positional_parameters = (1, 2)
    conversion = _create_default_conversion()
    
    class TestBuilder(BuilderBase):
        def _with_positional_parameters(self, input_positional_parameters):
            nonlocal positional_parameters
            nonlocal with_positional_parameters_called
            vampytest.assert_eq(positional_parameters, input_positional_parameters)
            with_positional_parameters_called = True
    
    builder = TestBuilder()
    
    output = builder._setter_positional(conversion, positional_parameters)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_true(with_positional_parameters_called)


def test__BuilderBase__setter_keyword():
    """
    Tests whether ``BuilderBase._setter_keyword`` works as intended.
    """
    with_keyword_parameters_called = False
    keyword_parameters = {1: 2}
    conversion = _create_default_conversion()
    
    class TestBuilder(BuilderBase):
        def _with_keyword_parameters(self, input_keyword_parameters):
            nonlocal keyword_parameters
            nonlocal with_keyword_parameters_called
            vampytest.assert_eq(keyword_parameters, input_keyword_parameters)
            with_keyword_parameters_called = True
            
    builder = TestBuilder()
    
    output = builder._setter_keyword(conversion, keyword_parameters)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_true(with_keyword_parameters_called)


def test__BuilderBase__with_positional_parameter_unknown():
    """
    Tests whether ``BuilderBase._with_positional_parameter_unknown`` works as intended.
    """
    value = object()
    
    builder = BuilderBase()
    
    output = builder._with_positional_parameter_unknown(value)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__BuilderBase__with_positional_parameters__no_match():
    """
    Tests whether ``BuilderBase._with_positional_parameters`` works as intended.
    
    Case: No match.
    """
    with_positional_parameter_unknown_called = False
    value = object()
    
    
    def set_identifier(value):
        return
        yield
    
    conversion = _create_default_conversion({
        'set_identifier': set_identifier,
    })
    
    class TestBuilder(BuilderBase):
        
        ayaya = conversion
        
        def _with_positional_parameter_unknown(self, input_value):
            nonlocal value
            nonlocal with_positional_parameter_unknown_called
            vampytest.assert_eq(value, input_value)
            with_positional_parameter_unknown_called = True
    
    builder = TestBuilder()
    
    builder._with_positional_parameters((value,))
    
    vampytest.assert_true(with_positional_parameter_unknown_called)
    

def test__BuilderBase__with_positional_parameters__identifier_match():
    """
    Tests whether ``BuilderBase._with_positional_parameters`` works as intended.
    
    Case: identifier matching it.
    """
    with_field_called = False
    value = object()
    
    
    def set_identifier(value):
        yield value
        return
    
    conversion = _create_default_conversion({
        'kind': CONVERSION_KIND_FIELD,
        'set_identifier': set_identifier,
    })
    
    class TestBuilder(BuilderBase):
        
        ayaya = conversion
        
        def _setter_field(self, input_conversion, input_value):
            nonlocal value
            nonlocal with_field_called
            nonlocal conversion
            vampytest.assert_eq(value, input_value)
            vampytest.assert_is(conversion, input_conversion)
            with_field_called = True
    
    builder = TestBuilder()
    
    builder._with_positional_parameters((value,))
    
    vampytest.assert_true(with_field_called)


def test__BuilderBase__with_positional_parameters__type_match():
    """
    Tests whether ``BuilderBase._with_positional_parameters`` works as intended.
    
    Case: type matching it.
    """
    with_field_called = False
    value = 1
    
    def set_type_processor(input_value):
        return input_value + 1
    
    conversion = _create_default_conversion({
        'set_type': type(value),
        'set_type_processor': set_type_processor,
        'kind': CONVERSION_KIND_FIELD
    })
    
    class TestBuilder(BuilderBase):
        
        ayaya = conversion
        
        def _setter_field(self, input_conversion, input_value):
            nonlocal value
            nonlocal with_field_called
            nonlocal conversion
            nonlocal set_type_processor
            vampytest.assert_eq(set_type_processor(value), input_value)
            vampytest.assert_is(conversion, input_conversion)
            with_field_called = True
    
    builder = TestBuilder()
    
    builder._with_positional_parameters((value,))
    
    vampytest.assert_true(with_field_called)


def test__BuilderBase__with_keyword_parameter_unknown():
    """
    Tests whether ``BuilderBase._with_keyword_parameter_unknown`` works as intended.
    """
    key = 'mister'
    value = object()
    
    builder = BuilderBase()
    
    output = builder._with_keyword_parameter_unknown(key, value)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__BuilderBase__with_keyword_parameters__no_match():
    """
    Tests whether ``BuilderBase._with_keyword_parameters`` works as intended.
    
    Case: No match.
    """
    with_keyword_parameter_unknown_called = False
    key = 'sanae'
    value = object()
    
    def set_validator(value):
        return
        yield
    
    conversion = _create_default_conversion({
        'set_validator': set_validator,
    })
    
    class TestBuilder(BuilderBase):
        
        ayaya = set_validator
        
        def _with_keyword_parameter_unknown(self, input_key, input_value):
            nonlocal key
            nonlocal value
            nonlocal with_keyword_parameter_unknown_called
            vampytest.assert_eq(value, input_value)
            vampytest.assert_eq(key, input_key)
            with_keyword_parameter_unknown_called = True
    
    builder = TestBuilder()
    
    builder._with_keyword_parameters({key: value})
    
    vampytest.assert_true(with_keyword_parameter_unknown_called)
    

def test__BuilderBase__with_keyword_parameters__match():
    """
    Tests whether ``BuilderBase._with_keyword_parameters`` works as intended.
    
    Case: matching
    """
    with_field_called = False
    name = 'sanae'
    value = object()
    
    def set_validator(value):
        yield value
        return
    
    conversion = _create_default_conversion({
        'name': name,
        'set_validator': set_validator,
        'kind': CONVERSION_KIND_FIELD,
    })
    
    class TestBuilder(BuilderBase):
        
        ayaya = conversion
        
        def _setter_field(self, input_conversion, input_value):
            nonlocal value
            nonlocal with_field_called
            nonlocal conversion
            vampytest.assert_eq(value, input_value)
            vampytest.assert_is(conversion, input_conversion)
            with_field_called = True
    
    builder = TestBuilder()
    
    builder._with_keyword_parameters({name: value})
    
    vampytest.assert_true(with_field_called)


def test__BuilderBase__getter_none():
    """
    Tests whether ``BuilderBase._getter_none`` works as intended.
    """
    builder = BuilderBase()
    conversion = _create_default_conversion()
    
    with vampytest.assert_raises(RuntimeError):
        builder._getter_none(conversion)


def test__BuilderBase__getter_field__no_processor():
    """
    Tests whether ``BuilderBase._getter_field`` works as intended.
    
    Case: No processor.
    """
    conversion = _create_default_conversion()
    value_to_pull = 1
    
    class TestBuilder(BuilderBase):
        def _try_pull_field_value(self, input_conversion):
            nonlocal value_to_pull
            nonlocal conversion
            vampytest.assert_is(conversion, input_conversion)
            yield value_to_pull
    
    
    builder = TestBuilder()
    output = builder._getter_field(conversion)
    
    vampytest.assert_instance(output, type(value_to_pull))
    vampytest.assert_eq(output, value_to_pull)


def test__BuilderBase__getter_field__with_processor():
    """
    Tests whether ``BuilderBase._getter_field`` works as intended.
    
    Case: With processor.
    """
    def get_processor(value):
        return value + 1
    
    conversion = _create_default_conversion({
        'get_processor': get_processor,
    })
    value_to_pull = 1
    
    
    class TestBuilder(BuilderBase):
        def _try_pull_field_value(self, input_conversion):
            nonlocal value_to_pull
            nonlocal conversion
            vampytest.assert_is(conversion, input_conversion)
            yield value_to_pull
    
    
    builder = TestBuilder()
    output = builder._getter_field(conversion)
    
    vampytest.assert_instance(output, type(value_to_pull))
    vampytest.assert_eq(output, get_processor(value_to_pull))


def test__BuilderBase__getter_field__default():
    """
    Tests whether ``BuilderBase._getter_field`` works as intended.
    
    Case: default.
    """
    get_default = 11
    conversion = _create_default_conversion({
        'get_default': get_default,
    })
    
    class TestBuilder(BuilderBase):
        def _try_pull_field_value(self, input_conversion):
            vampytest.assert_is(conversion, input_conversion)
            return
            yield
    
    
    builder = TestBuilder()
    output = builder._getter_field(conversion)
    
    vampytest.assert_instance(output, type(get_default))
    vampytest.assert_eq(get_default, get_default)


def test__BuilderBase__setter_instance():
    """
    Tests whether ``BuilderBase._setter_instance`` works as intended.
    """
    conversion_0 = _create_default_conversion()
    conversion_1 = _create_default_conversion()
    conversion_2 = _create_default_conversion()
    
    value_0 = 1
    value_1 = 69
    
    input = []
    
    class TestBuilder(BuilderBase):
        def _setter_field(self, input_conversion, input_value):
            nonlocal input
            input.append((input_conversion, input_value))
            return True
        
        
        def _iter_fields(self):
            nonlocal conversion_0
            nonlocal conversion_1
            nonlocal value_0
            nonlocal value_1
            
            yield conversion_0, value_0
            yield conversion_1, value_1
    
    builder = TestBuilder()
    
    # We ignore the conversion here, so it can be anything.s
    builder._setter_instance(conversion_2, TestBuilder())
    
    vampytest.assert_eq(
        input,
        [(conversion_0, value_0), (conversion_1, value_1)],
    )


def test__BuilderBase__iter_conversions():
    """
    Tests whether ``BuilderBase._iter_conversions`` works as intended.
    """
    vampytest.assert_true(is_generator_function(BuilderBase._iter_conversions))


def test__BuilderBase__iter_fields():
    """
    Tests whether ``BuilderBase._iter_fields`` works as intended.
    """
    vampytest.assert_true(is_generator_function(BuilderBase._iter_fields))


def test__BuilderBase__try_match_as_typed__hit():
    """
    Tests whether ``BuilderBase._try_match_as_typed`` works as intended.
    
    Case: hit.
    """
    conversion = _create_default_conversion({
        'kind': CONVERSION_KIND_FIELD,
        'set_type': int,
    })
    
    value = 1
    
    input = []
    
    class TestBuilder(BuilderBase):
        flags = conversion
        
        def _setter_field(self, input_conversion, input_value):
            nonlocal input
            input.append((input_conversion, input_value))
            return True
    
    
    builder = TestBuilder()
    
    # We ignore the conversion here, so it can be anything.s
    output = builder._try_match_as_typed(value)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_eq(
        input,
        [(conversion, value)],
    )


def test__BuilderBase__try_match_as_typed__miss():
    """
    Tests whether ``BuilderBase._try_match_as_typed`` works as intended.
    
    Case: miss.
    """
    conversion = _create_default_conversion({
        'kind': CONVERSION_KIND_FIELD,
        'set_type': int,
    })
    
    value = '1'
    
    input = []
    
    class TestBuilder(BuilderBase):
        flags = conversion
        
        def _setter_field(self, input_conversion, input_value):
            nonlocal input
            input.append((input_conversion, input_value))
            return True
    
    
    builder = TestBuilder()
    
    # We ignore the conversion here, so it can be anything.s
    output = builder._try_match_as_typed(value)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    vampytest.assert_eq(
        input,
        [],
    )


def test__BuilderBase__try_match_as_listing__hit():
    """
    Tests whether ``BuilderBase._try_match_as_listing`` works as intended.
    
    Case: hit.
    """
    def set_listing_identifier(value):
        for element in value:
            if not isinstance(element, int):
                return
        
        yield value
    
    
    conversion = _create_default_conversion({
        'kind': CONVERSION_KIND_FIELD,
        'set_listing_identifier': set_listing_identifier,
    })
    
    value = [1]
    
    input = []
    
    class TestBuilder(BuilderBase):
        flags = conversion
        
        def _setter_field(self, input_conversion, input_value):
            nonlocal input
            input.append((input_conversion, input_value))
            return True
    
    
    builder = TestBuilder()
    
    # We ignore the conversion here, so it can be anything.s
    output = builder._try_match_as_listing(value)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_eq(
        input,
        [(conversion, value)],
    )


def test__BuilderBase__try_match_as_listing__miss():
    """
    Tests whether ``BuilderBase._try_match_as_listing`` works as intended.
    
    Case: miss.
    """
    def set_listing_identifier(value):
        for element in value:
            if not isinstance(element, int):
                return
        
        yield value
    
    
    conversion = _create_default_conversion({
        'kind': CONVERSION_KIND_FIELD,
        'set_listing_identifier': set_listing_identifier,
    })
    
    value = ['1']
    
    input = []
    
    class TestBuilder(BuilderBase):
        flags = conversion
        
        def _setter_field(self, input_conversion, input_value):
            nonlocal input
            input.append((input_conversion, input_value))
            return True
    
    
    builder = TestBuilder()
    
    # We ignore the conversion here, so it can be anything.s
    output = builder._try_match_as_listing(value)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    vampytest.assert_eq(
        input,
        [],
    )


def test__BuilderBase__try_match_as_sub_type__hit():
    """
    Tests whether ``BuilderBase._try_match_as_sub_type`` works as intended.
    
    Case: hit.
    """
    conversion = _create_default_conversion({
        'kind': CONVERSION_KIND_FIELD,
        'set_type': int,
    })
    
    value = True
    
    input = []
    
    class TestBuilder(BuilderBase):
        flags = conversion
        
        def _setter_field(self, input_conversion, input_value):
            nonlocal input
            input.append((input_conversion, input_value))
            return True
    
    
    builder = TestBuilder()
    
    # We ignore the conversion here, so it can be anything.s
    output = builder._try_match_as_sub_type(value)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_eq(
        input,
        [(conversion, True)],
    )
    
    vampytest.assert_is(builder.DESCRIPTORS_TYPED[int], builder.DESCRIPTORS_TYPED.get(bool, None))


def test__BuilderBase__try_match_as_sub_type__miss():
    """
    Tests whether ``BuilderBase._try_match_as_sub_type`` works as intended.
    
    Case: hit.
    """
    conversion = _create_default_conversion({
        'kind': CONVERSION_KIND_FIELD,
        'set_type': int,
    })
    
    value = 'True'
    
    input = []
    
    class TestBuilder(BuilderBase):
        flags = conversion
        
        def _setter_field(self, input_conversion, input_value):
            nonlocal input
            input.append((input_conversion, input_value))
            return True
    
    
    builder = TestBuilder()
    
    # We ignore the conversion here, so it can be anything.s
    output = builder._try_match_as_sub_type(value)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    vampytest.assert_eq(
        input,
        [],
    )


def test__BuilderBase__try_match_as_identified__hit():
    """
    Tests whether ``BuilderBase._try_match_as_identified`` works as intended.
    
    Case: hit.
    """
    def set_identifier(value):
        if value == 2:
            yield value
    
    conversion = _create_default_conversion({
        'kind': CONVERSION_KIND_FIELD,
        'set_identifier': set_identifier,
    })
    
    value = 2
    
    input = []
    
    class TestBuilder(BuilderBase):
        flags = conversion
        
        def _setter_field(self, input_conversion, input_value):
            nonlocal input
            input.append((input_conversion, input_value))
            return True
    
    
    builder = TestBuilder()
    
    # We ignore the conversion here, so it can be anything.s
    output = builder._try_match_as_identified(value)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_eq(
        input,
        [(conversion, 2)],
    )


def test__BuilderBase__try_match_as_identified__miss():
    """
    Tests whether ``BuilderBase._try_match_as_identified`` works as intended.
    
    Case: miss.
    """
    def set_identifier(value):
        if value == 2:
            yield value
    
    conversion = _create_default_conversion({
        'kind': CONVERSION_KIND_FIELD,
        'set_identifier': set_identifier,
    })
    
    value = 1
    
    input = []
    
    class TestBuilder(BuilderBase):
        flags = conversion
        
        def _setter_field(self, input_conversion, input_value):
            nonlocal input
            input.append((input_conversion, input_value))
            return True
    
    
    builder = TestBuilder()
    
    # We ignore the conversion here, so it can be anything.s
    output = builder._try_match_as_identified(value)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    vampytest.assert_eq(
        input,
        [],
    )



def test__BuilderBase__serialize():
    """
    Tests whether ``BuilderBase.serialise`` works as intended.
    """
    def serializer_optional(value):
        if value:
            yield value
    
    def serializer_required(value):
        return value

    conversion_0 = _create_default_conversion({
        'name': 'koishi',
        'kind': CONVERSION_KIND_FIELD,
        'serializer_key': 'koishi',
        'serializer_optional': serializer_optional,
        'serializer_required': serializer_required,
    })
    conversion_1 = _create_default_conversion({
        'name': 'satori',
        'kind': CONVERSION_KIND_FIELD,
        'serializer_key': 'satori',
        'serializer_optional': serializer_optional,
        'serializer_required': serializer_required,
    })
    conversion_2 = _create_default_conversion({
        'name': 'orin',
        'kind': CONVERSION_KIND_FIELD,
        'serializer_key': 'orin',
        'serializer_optional': serializer_optional,
        'serializer_required': serializer_required,
    })
    
    value_0 = 0
    value_1 = 1
    value_2 = None
    
    value_table = {
        conversion_0: value_0,
        conversion_1: value_1,
        conversion_2: value_2,
    }
    
    class TestBuilder(BuilderBase):
        koishi = conversion_0
        satori = conversion_1
        orin = conversion_2
        
        
        def _try_pull_field_value(self, input_conversion):
            nonlocal value_table
            value = value_table.get(input_conversion, None)
            if (value is not None):
                yield value
    
    builder = TestBuilder()
    
    output = builder.serialise(
        SerializationConfiguration([TestBuilder.koishi, TestBuilder.satori, TestBuilder.orin], True)
    )
    vampytest.assert_eq(
        output,
        {'koishi': value_0, 'satori': value_1}
    )

    output = builder.serialise(
        SerializationConfiguration([TestBuilder.koishi, TestBuilder.orin], False)
    )
    vampytest.assert_eq(
        output,
        {}
    )
