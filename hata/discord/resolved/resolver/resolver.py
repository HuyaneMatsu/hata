__all__ = ('Resolver',)

from scarletio import RichAttributeErrorBaseType


class Resolver(RichAttributeErrorBaseType):
    """
    Holds resolver functions for interacting with a resolver.
    
    Attributes
    ----------
    iter_resolve_multiple : ``GeneratorFunctionType``
        Iterable generator for iterating over multiple resolved instances.
    
    iter_resolve_single : ``GeneratorFunctionType``
        Iterable generator for iterating over a single resolved instance.
    
    name : `str`
        The name of the resolver.
    
    resolve_multiple : ``FunctionType``
        Resolver for resolving multiple instances.
    
    resolve_single : ``FunctionType``
        Resolver for resolving a single instance.
    """
    __slots__ = ('iter_resolve_multiple', 'iter_resolve_single', 'name', 'resolve_multiple', 'resolve_single')
    
    def __new__(cls, name, resolve_single, iter_resolve_single, resolve_multiple, iter_resolve_multiple):
        """
        Creates a new resolver instance.
        
        Parameters
        ----------
        name : `str`
            The name of the resolver.
        
        resolve_single : ``FunctionType``
            Resolver for resolving a single instance.
        
        iter_resolve_single : ``GeneratorFunctionType``
            Iterable generator for iterating over a single resolved instance.
        
        resolve_multiple : ``FunctionType``
            Resolver for resolving multiple instances.
        
        iter_resolve_multiple : ``GeneratorFunctionType``
            Iterable generator for iterating over multiple resolved instances.
        """
        self = object.__new__(cls)
        self.iter_resolve_multiple = iter_resolve_multiple
        self.iter_resolve_single = iter_resolve_single
        self.name = name
        self.resolve_multiple = resolve_multiple
        self.resolve_single = resolve_single
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        return f'<{type(self).__name__} {self.name!s}>'
