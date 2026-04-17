from types import FunctionType

import vampytest

from ..resolver import Resolver


def _assert_fields_set(resolver):
    """
    Asserts whether the given instance has all of its fields ste.
    
    Parameters
    ----------
    resolver : ``Resolver``
        The instance to check.
    """
    vampytest.assert_instance(resolver, Resolver)
    vampytest.assert_instance(resolver.iter_resolve_multiple, FunctionType)
    vampytest.assert_instance(resolver.iter_resolve_single, FunctionType)
    vampytest.assert_instance(resolver.name, str)
    vampytest.assert_instance(resolver.resolve_multiple, FunctionType)
    vampytest.assert_instance(resolver.resolve_single, FunctionType)


def test__Resolver__new():
    """
    Tests whether ``Resolver.__new__`` works as intended.
    """
    name = 'potato'
    
    def resolve_single(resolved, value):
        return
    
    def iter_resolve_single(resolved, value):
        return
        yield
    
    def resolve_multiple(resolved, values):
        return
    
    def iter_resolve_multiple(resolved, values):
        return
        yield
    
    resolver = Resolver( name, resolve_single, iter_resolve_single, resolve_multiple, iter_resolve_multiple)
    _assert_fields_set(resolver)
    
    vampytest.assert_is(resolver.iter_resolve_multiple, iter_resolve_multiple)
    vampytest.assert_is(resolver.iter_resolve_single, iter_resolve_single)
    vampytest.assert_is(resolver.name, name)
    vampytest.assert_is(resolver.resolve_multiple, resolve_multiple)
    vampytest.assert_is(resolver.resolve_single, resolve_single)


def test__Resolver__repr():
    """
    Tests whether ``Resolver.__repr__`` works as intended.
    """
    name = 'potato'
    
    def resolve_single(resolved, value):
        return
    
    def iter_resolve_single(resolved, value):
        return
        yield
    
    def resolve_multiple(resolved, values):
        return
    
    def iter_resolve_multiple(resolved, values):
        return
        yield
    
    resolver = Resolver( name, resolve_single, iter_resolve_single, resolve_multiple, iter_resolve_multiple)
    
    output = repr(resolver)
    vampytest.assert_instance(output, str)
