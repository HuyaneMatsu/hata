import vampytest

from ..constants import CONVERSION_KIND_FIELD
from ..builder_fielded import BuilderFielded

from .helpers import _create_default_conversion


def _assert_fields_set(message_builder):
    """
    Asserts whether every fields of the message builder are set.
    
    Parameters
    ----------
    message_builder : ``BuilderFielded``
        The message builder to test.
    """
    vampytest.assert_instance(message_builder, BuilderFielded)
    vampytest.assert_instance(message_builder.fields, dict)


def test__BuilderFielded__new():
    """
    Tests whether ``BuilderFielded.__new__`` works as intended.
    """
    message_builder = BuilderFielded()
    _assert_fields_set(message_builder)


def test__BuilderFielded__store_field_value():
    """
    Tests whether ``BuilderFielded._store_field_value`` works as intended.
    """
    conversion = _create_default_conversion({
        'field_kind': CONVERSION_KIND_FIELD,
        'set_type': str,
    })
    value = 'hes mister'
    
    message_builder = BuilderFielded()
    message_builder._store_field_value(conversion, value)
    
    vampytest.assert_eq(
        message_builder.fields,
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
    
    message_builder = BuilderFielded()
    
    for item in []:
        message_builder._store_field_value(*item)
    
    output = [*message_builder._try_pull_field_value(conversion)]
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
    
    message_builder = BuilderFielded()
    
    message_builder._store_field_value(conversion, 'mister')
    
    output = [*message_builder._try_pull_field_value(conversion)]
    vampytest.assert_eq(output, ['mister'])


def test__BuilderFielded__with_positional_parameter_unknown():
    """
    Tests whether ``BuilderFielded._with_positional_parameter_unknown`` works as intended.
    """
    value = [12] 
    
    message_builder = BuilderFielded()
    
    with vampytest.assert_raises(TypeError):
        message_builder._with_positional_parameter_unknown(value)


def test__BuilderFielded__with_keyword_parameter_unknown():
    """
    Tests whether ``BuilderFielded._with_keyword_parameter_unknown`` works as intended.
    """
    key = 'mister'
    value = [12] 
    
    message_builder = BuilderFielded()
    
    with vampytest.assert_raises(TypeError):
        message_builder._with_keyword_parameter_unknown(key, value)


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
    message_builder = BuilderFielded()
    
    
    for item in fields:
        message_builder._store_field_value(*item)
    
    output = [*message_builder._iter_fields()]
    
    vampytest.assert_eq(
        dict(fields),
        dict(output),
    )
