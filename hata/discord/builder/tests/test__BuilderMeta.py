import vampytest

from ..builder_base import BuilderMeta
from ..descriptor import ConversionDescriptor

from .helpers import _create_default_conversion


def test__BuilderMeta__new__conversions_collection__initial():
    """
    Tests whether ``BuilderMeta.__new__`` works as intended.
    
    Case: Conversion collection & initial.
    """
    conversion_0 = _create_default_conversion({
        'name': 'flags',
    })
    conversion_1 = _create_default_conversion({
        'name': 'mister',
    })
    
    
    class test_type(metaclass = BuilderMeta):
        __slots__ = ()
        
        flags = conversion_0
        type = conversion_1
        
        def _setter_none(self, conversion, value):
            raise RuntimeError
        
        
        def _getter_none(self, conversion):
            raise RuntimeError
    
    
    vampytest.assert_instance(test_type, BuilderMeta)
    
    vampytest.assert_instance(test_type.flags, ConversionDescriptor)
    vampytest.assert_instance(test_type.type, ConversionDescriptor)
    
    vampytest.assert_is(test_type.flags.conversion, conversion_0)
    vampytest.assert_is(test_type.type.conversion, conversion_1)
    
    vampytest.assert_instance(test_type.CONVERSIONS_ASSIGNED, dict)
    vampytest.assert_eq(
        test_type.CONVERSIONS_ASSIGNED,
        {
            'flags':  conversion_0,
            'type': conversion_1,
        },
    )


def test__BuilderMeta__new__conversions_collection__inheritance():
    """
    Tests whether ``BuilderMeta.__new__`` works as intended.
    
    Case: Conversion collection & inheritance.
    """
    conversion_0 = _create_default_conversion({
        'name': 'flags',
    })
    conversion_1 = _create_default_conversion({
        'name': 'mister',
    })
    
    
    class test_type_0(metaclass = BuilderMeta):
        __slots__ = ()
        
        flags = conversion_0
        
        
        def _setter_none(self, conversion, value):
            raise RuntimeError
        
        
        def _getter_none(self, conversion):
            raise RuntimeError
    
    
    class test_type_1(metaclass = BuilderMeta):
        __slots__ = ()
        
        type = conversion_1
        
        
        def _setter_none(self, conversion, value):
            raise RuntimeError
        
        
        def _getter_none(self, conversion):
            raise RuntimeError
    
    
    class test_type(test_type_0, test_type_1):
        __slots__ = ()
    
    
    vampytest.assert_instance(test_type, BuilderMeta)
    
    vampytest.assert_instance(test_type.flags, ConversionDescriptor)
    vampytest.assert_instance(test_type.type, ConversionDescriptor)
    
    vampytest.assert_is(test_type.flags.conversion, conversion_0)
    vampytest.assert_is(test_type.type.conversion, conversion_1)
    
    vampytest.assert_instance(test_type.CONVERSIONS_ASSIGNED, dict)
    vampytest.assert_eq(
        test_type.CONVERSIONS_ASSIGNED,
        {
            'flags':  conversion_0,
            'type': conversion_1,
        },
    )


def test__BuilderMeta__new__DESCRIPTORS_POSITIONAL():
    """
    Tests whether ``BuilderMeta.__new__`` works as intended.
    
    Case: Check ``DESCRIPTORS_POSITIONAL``.
    """
    def set_identifier(value):
        yield value
    
    conversion_0 = _create_default_conversion({
        'name': 'flags',
    })
    conversion_1 = _create_default_conversion({
        'name': 'mister',
        'set_identifier': set_identifier,
    })
    
    class test_type(metaclass = BuilderMeta):
        __slots__ = ()
        
        flags = conversion_0
        type = conversion_1
        
        def _setter_none(self, conversion, value):
            raise RuntimeError
        
        
        def _getter_none(self, conversion):
            raise RuntimeError
    
    
    vampytest.assert_instance(test_type, BuilderMeta)
    
    vampytest.assert_instance(test_type.DESCRIPTORS_POSITIONAL, list)
    
    vampytest.assert_eq(
        {descriptor.conversion for descriptor in test_type.DESCRIPTORS_POSITIONAL},
        {conversion_1},
    )


def test__BuilderMeta__new__DESCRIPTORS_KEYWORD():
    """
    Tests whether ``BuilderMeta.__new__`` works as intended.
    
    Case: Check ``DESCRIPTORS_KEYWORD``.
    """
    def set_validator(value):
        yield value
    
    
    conversion_0 = _create_default_conversion({
        'name': 'flags',
    })
    conversion_1 = _create_default_conversion({
        'name': 'mister',
        'set_validator': set_validator,
        'name_aliases': ('hey', 'sister',),
    })
    
    
    class test_type(metaclass = BuilderMeta):
        __slots__ = ()
        
        flags = conversion_0
        type = conversion_1
        
        def _setter_none(self, conversion, value):
            raise RuntimeError
        
        
        def _getter_none(self, conversion):
            raise RuntimeError
    
    
    vampytest.assert_instance(test_type, BuilderMeta)
    
    vampytest.assert_instance(test_type.DESCRIPTORS_KEYWORD, dict)
    
    vampytest.assert_eq(
        {name: descriptor.conversion for name, descriptor in test_type.DESCRIPTORS_KEYWORD.items()},
        {'hey': conversion_1, 'sister': conversion_1, 'mister': conversion_1},
    )


def test__BuilderMeta__new__DESCRIPTORS_TYPED():
    """
    Tests whether ``BuilderMeta.__new__`` works as intended.
    
    Case: Check `DESCRIPTORS_TYPED` and `DESCRIPTORS_TYPED_ORDERED`.
    """
    conversion_0 = _create_default_conversion({
        'name': 'flags',
        'set_type': int,
        'sort_priority': 2,
    })
    conversion_1 = _create_default_conversion({
        'name': 'mister',
        'set_type': str,
        'sort_priority': 1
    })
    conversion_2 = _create_default_conversion({
        'name': 'pudding',
    })
    
    
    class test_type(metaclass = BuilderMeta):
        __slots__ = ()
        
        flags = conversion_0
        type = conversion_1
        pudding = conversion_2
        
        def _setter_none(self, conversion, value):
            raise RuntimeError
        
        
        def _getter_none(self, conversion):
            raise RuntimeError
    
    
    vampytest.assert_instance(test_type, BuilderMeta)
    
    vampytest.assert_instance(test_type.DESCRIPTORS_TYPED, dict)
    
    vampytest.assert_eq(
        {key: descriptor.conversion for key, descriptor in test_type.DESCRIPTORS_TYPED.items()},
        {int: conversion_0, str: conversion_1},
    )

    vampytest.assert_instance(test_type.DESCRIPTORS_TYPED_ORDERED, list)
    
    vampytest.assert_eq(
        [descriptor.conversion for descriptor in test_type.DESCRIPTORS_TYPED_ORDERED],
        [conversion_1, conversion_0],
    )


def test__BuilderMeta__new__DESCRIPTORS_LISTING():
    """
    Tests whether ``BuilderMeta.__new__`` works as intended.
    
    Case: Check `DESCRIPTORS_LISTING`.
    """
    def set_listing_identifier(value):
        yield value
        return
    
    conversion_0 = _create_default_conversion({
        'name': 'flags',
        'set_listing_identifier': set_listing_identifier,
        'sort_priority': 2,
    })
    conversion_1 = _create_default_conversion({
        'name': 'mister',
        'set_listing_identifier': set_listing_identifier,
        'sort_priority': 1
    })
    conversion_2 = _create_default_conversion({
        'name': 'pudding',
    })
    
    
    class test_type(metaclass = BuilderMeta):
        __slots__ = ()
        
        flags = conversion_0
        type = conversion_1
        pudding = conversion_2
        
        def _setter_none(self, conversion, value):
            raise RuntimeError
        
        
        def _getter_none(self, conversion):
            raise RuntimeError
    
    
    vampytest.assert_instance(test_type, BuilderMeta)
    
    vampytest.assert_instance(test_type.DESCRIPTORS_LISTING, list)
    
    vampytest.assert_eq(
        [descriptor.conversion for descriptor in test_type.DESCRIPTORS_LISTING],
        [conversion_1, conversion_0],
    )
