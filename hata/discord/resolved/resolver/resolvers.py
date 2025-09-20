__all__ = ()

from ..resolved import Resolved

from .resolver import Resolver


def _string_resolve_single(resolved, value):
    """
    String resolver for single value.
    
    Parameters
    ----------
    resolved : ``None | Resolved``
        Resolved to use.
    
    value : `None | str`
        Value to resolve.
    
    Returns
    -------
    value : `None | str`
    """
    return value


def _string_iter_resolve_single(resolved, value):
    """
    Iterative string resolver for single value.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    resolved : ``None | Resolved``
        Resolved to use.
    
    value : `None | str`
        Value to resolve.
    
    Yields
    -------
    value : `str`
    """
    if value is None:
        return
    
    yield value


def _string_resolve_multiple(resolved, values):
    """
    String resolver for multiple values.
    
    Parameters
    ----------
    resolved : ``None | Resolved``
        Resolved to use.
    
    values : `None | tuple<str>`
        Values to resolve.
    
    Returns
    -------
    values : `None | tuple<str>`
    """
    return values


def _iter_resolve_string_multiple(resolved, values):
    """
    Iterative string resolver for multiple values.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    resolved : ``None | Resolved``
        Resolved to use.
    
    values : `None | tuple<str>`
        Values to resolve.
    
    Yields
    -------
    value : `str`
    """
    if values is None:
        return
    
    yield from values


def _entity_resolver_factory(resolver_function):
    """
    Creates resolver functions with the given resolver function. 
    
    Parameters
    ----------
    resolver_function : ``FunctionType``
        Resolver function to use.
    
    Returns
    -------
    resolver_functions : `(FunctionType, FunctionType, FunctionType, FunctionType)`
    """
    def _entity_resolve_single(resolved, value):
        """
        Entity resolver for single value.
        
        Parameters
        ----------
        resolved : ``None | Resolved``
            Resolved to use.
        
        value : `None | str`
            Value to resolve.
        
        Returns
        -------
        value : `None | resolver_function.return`
        """
        nonlocal resolver_function
        
        if (resolved is None):
            return
        
        if (value is None):
            return
        
        try:
            entity_id = int(value)
        except ValueError:
            return
        
        return resolver_function(resolved, entity_id)
    
    
    def _entity_iter_resolve_single(resolved, value):
        """
        Iterative entity resolver for single value.
        
        This function is an iterable generator.
        
        Parameters
        ----------
        resolved : ``None | Resolved``
            Resolved to use.
        
        value : `None | str`
            Value to resolve.
        
        Yields
        -------
        value : `resolver_function.return`
        """
        nonlocal resolver_function
        
        if (resolved is None):
            return
        
        if (value is None):
            return
        
        try:
            entity_id = int(value)
        except ValueError:
            return
        
        entity = resolver_function(resolved, entity_id)
        if entity is None:
            return
        
        yield entity
    
    
    def _entity_resolve_multiple(resolved, values):
        """
        Entity resolver for multiple values.
        
        Parameters
        ----------
        resolved : ``None | Resolved``
            Resolved to use.
        
        values : `None | tuple<str>`
            Values to resolve.
        
        Returns
        -------
        values : `None | tuple<resolver_function.return>`
        """
        nonlocal resolver_function
        
        if (resolved is None):
            return
        
        if (values is None):
            return
        
        entities = None
        
        for value in values:
            try:
                entity_id = int(value)
            except ValueError:
                continue
            
            entity = resolver_function(resolved, entity_id)
            if entity is None:
                continue
            
            if entities is None:
                entities = []
            
            entities.append(entity)
            continue
        
        if (entities is not None):
            entities = tuple(entities)
        
        return entities
    
    
    def _entity_iter_resolve_multiple(resolved, values):
        """
        Iterative entity resolver for multiple values.
        
        This function is an iterable generator.
        
        Parameters
        ----------
        resolved : ``None | Resolved``
            Resolved to use.
        
        values : `None | tuple<str>`
            Values to resolve.
        
        Yields
        -------
        value : `resolver_function.return`
        """
        nonlocal resolver_function
        
        if (resolved is None):
            return
        
        if (values is None):
            return
        
        for value in values:
            try:
                entity_id = int(value)
            except ValueError:
                continue
            
            entity = resolver_function(resolved, entity_id)
            if entity is None:
                continue
            
            yield entity
            continue
    
    return _entity_resolve_single, _entity_iter_resolve_single, _entity_resolve_multiple, _entity_iter_resolve_multiple


RESOLVER_STRING = Resolver(
    'string',
    _string_resolve_single,
    _string_iter_resolve_single,
    _string_resolve_multiple,
    _iter_resolve_string_multiple,
)


RESOLVER_ATTACHMENT = Resolver(
    'attachment',
    *_entity_resolver_factory(Resolved.resolve_attachment),
)

RESOLVER_CHANNEL = Resolver(
    'channel',
    *_entity_resolver_factory(Resolved.resolve_channel),
)

RESOLVER_ROLE = Resolver(
    'role',
    *_entity_resolver_factory(Resolved.resolve_role),
)

RESOLVER_MENTIONABLE = Resolver(
    'mentionable',
    *_entity_resolver_factory(Resolved.resolve_mentionable),
)

RESOLVER_MESSAGE = Resolver(
    'message',
    *_entity_resolver_factory(Resolved.resolve_message),
)

RESOLVER_USER = Resolver(
    'user',
    *_entity_resolver_factory(Resolved.resolve_user),
)
