from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..event_deprecation import EventDeprecation
from ..event_deprecation_descriptor import EventDeprecationDescriptor


def _assert_fields_set(event_deprecation_descriptor):
    """
    Checks whether every attribute is set of the given event deprecation.
    
    Parameters
    ----------
    event_deprecation_descriptor : ``EventDeprecationDescriptor``
        The instance to check.
    """
    vampytest.assert_instance(event_deprecation_descriptor, EventDeprecationDescriptor)
    vampytest.assert_instance(event_deprecation_descriptor.deprecation, EventDeprecation)
    vampytest.assert_instance(event_deprecation_descriptor.name, str)
    

def test__EventDeprecationDescriptor__new():
    """
    Tests whether ``EventDeprecationDescriptor.__new__`` works as intended.
    """
    deprecation = EventDeprecation(
        'koishi',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    name = 'satori'
    
    event_deprecation_descriptor = EventDeprecationDescriptor(name, deprecation)
    _assert_fields_set(event_deprecation_descriptor)
    vampytest.assert_eq(event_deprecation_descriptor.deprecation, deprecation)
    vampytest.assert_eq(event_deprecation_descriptor.name, name)
    

def test__EventDeprecationDescriptor__repr():
    """
    Tests whether ``EventDeprecationDescriptor.__repr__`` works as intended.
    """
    deprecation = EventDeprecation(
        'koishi',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    name = 'satori'
    
    event_deprecation_descriptor = EventDeprecationDescriptor(name, deprecation)
    
    output = repr(event_deprecation_descriptor)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(event_deprecation_descriptor).__name__, output)
    vampytest.assert_in(f'deprecation = {deprecation!r}', output)
    vampytest.assert_in(f'name = {name!r}', output)


def _iter_options__eq():
    deprecation = EventDeprecation(
        'koishi',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    name = 'satori'
    
    keyword_parameters = {
        'deprecation': deprecation,
        'name': name,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'deprecation': EventDeprecation(
                'orin',
                DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
            )
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'okuu',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__EventDeprecationDescriptor__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``EventDeprecationDescriptor.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    event_deprecation_descriptor_0 = EventDeprecationDescriptor(**keyword_parameters_0)
    event_deprecation_descriptor_1 = EventDeprecationDescriptor(**keyword_parameters_1)
    
    output = event_deprecation_descriptor_0 == event_deprecation_descriptor_1
    vampytest.assert_instance(output, bool)
    return output


def test__EventDeprecationDescriptor__hash():
    """
    Tests whether ``EventDeprecationDescriptor.__hash__`` works as intended.
    """
    deprecation = EventDeprecation(
        'koishi',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    name = 'satori'
    
    event_deprecation_descriptor = EventDeprecationDescriptor(name, deprecation)
    
    output = hash(event_deprecation_descriptor)
    vampytest.assert_instance(output, int)
