import vampytest

from ..constants import CONVERSION_KIND_FIELD
from ..builder_fielded import BuilderFielded

from .helpers import _create_default_conversion


def _assert_fields_set(builder):
    """
    Asserts whether every fields of the message builder are set.
    
    Parameters
    ----------
    builder : ``BuilderFielded``
        The message builder to test.
    """
    vampytest.assert_instance(builder, BuilderFielded)
    vampytest.assert_instance(builder.fields, dict)


def test__BuilderFielded__new():
    """
    Tests whether ``BuilderFielded.__new__`` works as intended.
    """
    builder = BuilderFielded()
    _assert_fields_set(builder)


def test__BuilderFielded__eq__same_type():
    """
    Tests whether ``BuilderFielded.__eq__`` works as intended.
    
    Case: Same type.
    """
    conversion = _create_default_conversion({
        'field_kind': CONVERSION_KIND_FIELD,
        'set_type': str,
    })
    
    builder_0 = BuilderFielded()
    builder_0._store_field_value(conversion, 'mister')
    builder_1 = BuilderFielded()
    builder_1._store_field_value(conversion, 'mister')
    builder_2 = BuilderFielded()
    
    output = builder_0 == builder_1
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    output = builder_0 == builder_2
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__BuilderFielded__eq__different_type():
    """
    Tests whether ``BuilderFielded.__eq__`` works as intended.
    
    Case : different type.
    """
    builder = BuilderFielded()
    
    output = builder == object()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__BuilderFielded__hash():
    """
    Tests whether ``BuilderFielded.__hash__`` works as intended.
    """
    conversion = _create_default_conversion({
        'field_kind': CONVERSION_KIND_FIELD,
        'set_type': str,
    })
    
    builder = BuilderFielded()
    builder._store_field_value(conversion, 'mister')
    
    output = hash(builder)
    vampytest.assert_instance(output, int)


def test__BuilderFielded__repr():
    """
    Tests whether ``BuilderFielded.__repr__`` works as intended.
    """
    conversion = _create_default_conversion({
        'field_kind': CONVERSION_KIND_FIELD,
        'set_type': str,
    })
    
    builder = BuilderFielded()
    builder._store_field_value(conversion, 'mister')
    
    output = repr(builder)
    vampytest.assert_instance(output, str)


def test__BuilderFielded__store_field_value():
    """
    Tests whether ``BuilderFielded._store_field_value`` works as intended.
    """
    conversion = _create_default_conversion({
        'field_kind': CONVERSION_KIND_FIELD,
        'set_type': str,
    })
    value = 'hes mister'
    
    builder = BuilderFielded()
    builder._store_field_value(conversion, value)
    
    vampytest.assert_eq(
        builder.fields,
        {
            conversion : value,
        },
    )


def test__BuilderFielded__try_pull_field_value__none():
    """
    Tests whether ``BuilderFielded._try_pull_field_value`` works as intended.
    
    Case: none.
    """
    conversion = _create_default_conversion({
        'field_kind': CONVERSION_KIND_FIELD,
        'set_type': str,
    })
    
    builder = BuilderFielded()
    
    for item in []:
        builder._store_field_value(*item)
    
    output = [*builder._try_pull_field_value(conversion)]
    vampytest.assert_eq(output, [])


def test__BuilderFielded__try_pull_field_value__match():
    """
    Tests whether ``BuilderFielded._try_pull_field_value`` works as intended.
    
    case: match.
    """
    conversion = _create_default_conversion({
        'field_kind': CONVERSION_KIND_FIELD,
        'set_type': str,
    })
    
    builder = BuilderFielded()
    
    builder._store_field_value(conversion, 'mister')
    
    output = [*builder._try_pull_field_value(conversion)]
    vampytest.assert_eq(output, ['mister'])


def test__BuilderFielded__with_positional_parameter_unknown():
    """
    Tests whether ``BuilderFielded._with_positional_parameter_unknown`` works as intended.
    """
    value = [12] 
    
    builder = BuilderFielded()
    
    with vampytest.assert_raises(TypeError):
        builder._with_positional_parameter_unknown(value)


def test__BuilderFielded__with_keyword_parameter_unknown():
    """
    Tests whether ``BuilderFielded._with_keyword_parameter_unknown`` works as intended.
    """
    key = 'mister'
    value = [12] 
    
    builder = BuilderFielded()
    
    with vampytest.assert_raises(TypeError):
        builder._with_keyword_parameter_unknown(key, value)


def test__BuilderFielded__iter_conversions():
    """
    Tests whether ``BuilderFielded._iter_conversions`` works as intended.
    """
    conversion_0 = _create_default_conversion({
        'field_kind': CONVERSION_KIND_FIELD,
        'set_type': str,
    })
    
    conversion_1 = _create_default_conversion({
        'field_kind': CONVERSION_KIND_FIELD,
        'set_type': str,
    })
    
    conversions = [(conversion_0, 'mister'), (conversion_1, 'hey')]
    builder = BuilderFielded()
    
    
    for item in conversions:
        builder._store_field_value(*item)
    
    output = {*builder._iter_conversions()}
    
    vampytest.assert_eq(
        {conversion[0] for conversion in conversions},
        output,
    )


def test__BuilderFielded__iter_fields():
    """
    Tests whether ``BuilderFielded._iter_fields`` works as intended.
    """
    conversion_0 = _create_default_conversion({
        'field_kind': CONVERSION_KIND_FIELD,
        'set_type': str,
    })
    
    conversion_1 = _create_default_conversion({
        'field_kind': CONVERSION_KIND_FIELD,
        'set_type': str,
    })
    
    fields = [(conversion_0, 'mister'), (conversion_1, 'hey')]
    builder = BuilderFielded()
    
    
    for item in fields:
        builder._store_field_value(*item)
    
    output = [*builder._iter_fields()]
    
    vampytest.assert_eq(
        dict(fields),
        dict(output),
    )
