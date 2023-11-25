__all__ = ('ClientWrapper',)

from scarletio import RichAttributeErrorBaseType

from ..core import CLIENTS

from .client import Client


def optimize_keyword_parameters(keyword_parameters):
    """
    Optimizes the given keyword parameters omitting ellipses.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to optimize.
    
    Returns
    -------
    keyword_parameters : `None | dict<str, object>`
    """
    keyword_parameters = {key: value for key, value in keyword_parameters.items() if value is not ...}
    if not keyword_parameters:
        keyword_parameters = None
    
    return keyword_parameters


class ClientWrapperEventsProxy(RichAttributeErrorBaseType):
    """
    When a client wrapper's `.events` is called without giving the `func` parameter to it an instance
    of this class is created for allowing using it as a decorator with passing additional keyword parameters at the
    same time.
    
    Attributes
    ----------
    called : `bool`
        Whether the poxy was already called and should fail the next time if `func` is not given.
    client_wrapper : ``ClientWrapper``
        The owner event descriptor.
    keyword_parameters: `None | dict<str, object>`
        Additional keyword parameters passed when the wrapper was created.
    """
    __slots__ = ('called', 'client_wrapper', 'keyword_parameters')
    
    def __new__(cls, client_wrapper, called, keyword_parameters):
        """
        Creates an instance from the given parameters.
        
        Parameters
        ----------
        client_wrapper : ``ClientWrapper``
            The owner client wrapper.
        keyword_parameters: `None | dict<str, object>`
            Additional keyword parameters passed when the wrapper was created.
        """
        self = object.__new__(cls)
        cls.called.__set__(self, called)
        cls.client_wrapper.__set__(self, client_wrapper)
        cls.keyword_parameters.__set__(self, keyword_parameters)
        return self
    
    
    def __call__(self, func = None, *, name = ..., overwrite = ...):
        """
        Adds the given `func` as event handler to the client_wrapper's clients' with the stored up parameters.
        
        Parameters
        ----------
        func : `callable`
            The event handler to add to the respective clients.
        
        Returns
        -------
        func : `None`, `callable` = `None`, Optional
            The event handler to add to the respective clients.
            
            If not given, will return a decorator.
        
        name : `None`, `str`, Optional (Keyword only)
            The name to which event the handler should be registered to.
            
            If not given, it will be extracted from the handler's name.
        
        overwrite : `bool`, Optional (Keyword only)
            Whether the current event handler(s) should be replaced by the added one.
        
        Returns
        -------
        output : `instance<type<self>>` / `func`
            The given an events proxy if `func` is `None` or omitted.
        
        Raises
        ------
        AttributeError
            - Invalid event name.
        TypeError
            - If a parameter's type is incorrect.
        """
        if self.called:
            if func is None:
                raise TypeError('`func` cannot be given as `None`.')
            
            keyword_parameters = self.keyword_parameters
        else:
            keyword_parameters = optimize_keyword_parameters({'name': name, 'overwrite': overwrite})
            
            if func is None:
                return type(self)(self.client_wrapper, True, keyword_parameters)
        
        for client in self.client_wrapper.clients:
            event_handler = client.events
            if keyword_parameters is None:
                event_handler(func)
            else:
                event_handler(func, **keyword_parameters)
        
        return func
        
    
    def __repr__(self):
        """Returns the proxy's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' client_wrapper = ')
        repr_parts.append(repr(self.client_wrapper))
        
        called = self.called
        if called:
            repr_parts.append(', called = ')
            repr_parts.append(repr(called))
        
        keyword_parameters = self.keyword_parameters
        if (keyword_parameters is not None):
            repr_parts.append(', keyword_parameters = ')
            repr_parts.append(repr(keyword_parameters))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the proxys are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.called != other.called:
            return False
        
        if self.client_wrapper != other.client_wrapper:
            return False
        
        if self.keyword_parameters != other.keyword_parameters:
            return False
        
        return True
    
    
    def __setattr__(self, attribute_name, attribute_value):
        """
        Sets an attribute of the wrapped client's event handler managers.
        
        Parameters
        ----------
        attribute_name : `str`
            The name of the event.
        attribute_value : `callable`
            The event handler.
        
        Raises
        ------
        AttributeError
            ``EventHandlerManager`` has no attribute named as the given `attribute_name`.
        """
        for client in self.client_wrapper.clients:
            client.events.__setattr__(attribute_name, attribute_value)
    
    
    def __delattr__(self, attribute_name):
        """
        Deletes an attribute of the wrapped client's event handler managers.
        
        Parameters
        ----------
        attribute_name : `str`
            The name of the event.
        
        Raises
        ------
        AttributeError
            ``EventHandlerManager`` has no attribute named as the given `attribute_name`.
        """
        for client in self.client_wrapper.clients:
            client.events.__delattr__(attribute_name)


class ClientWrapper(RichAttributeErrorBaseType):
    """
    Wraps together more clients enabling to add the same event handlers or commands to them. Tho for that feature, you
    need first import it's respective extension.
    
    Attributes
    ----------
    clients : ``Clients``
        The clients to wrap together.
    """
    __slots__ = ('clients',)
    
    def __new__(cls, *clients):
        """
        Creates a new ``ClientWrapper`` with the given clients. If no clients are given, then will wrap
        all the clients.
        
        Parameters
        ----------
        *clients : ``Client``
            The clients to wrap together.
        
        Raises
        ------
        TypeError
            A non ``Client`` was given.
        """
        if clients:
            for client in clients:
                if not isinstance(client, Client):
                    raise TypeError(
                        f'{cls.__name__} expects only `{Client.__name__}`, '
                        f'got {client.__class__.__name__}; {client!r}.'
                    )
        else:
            clients = tuple(CLIENTS.values())
        
        self = object.__new__(cls)
        self.clients = clients
        return self
    
    
    def __repr__(self):
        """Returns the client wrapper's representation."""
        result = [self.__class__.__name__, '(']
        
        clients = self.clients
        limit = len(clients)
        if limit:
            index = 0
            while True:
                client = clients[index]
                result.append(client.full_name)
                
                index += 1
                if index == limit:
                    break
                
                result.append(', ')
                continue
        
        result.append(')')
        
        return ''.join(result)
    
    
    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        
        return {*self.clients} == {*other.clients}
    
    
    def __iter__(self):
        """Iterates over the clients of the client wrapper."""
        yield from self.clients
    
    
    def __contains__(self, value):
        """Returns whether the client wrapper contains the given value."""
        return value in self.clients
    
    
    @property
    def events(self):
        """
        Returns an events proxy which enables adding / removing event handlers.
        
        Returns
        -------
        proxy : ``ClientWrapperEventsProxy``
        """
        return ClientWrapperEventsProxy(self, False, None)
