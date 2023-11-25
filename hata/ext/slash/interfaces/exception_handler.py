__all__ = ()

from functools import partial as partial_func

from scarletio import CallableAnalyzer, RichAttributeErrorBaseType


def test_exception_handler(exception_handler):
    """
    Tests whether the given exception handler accepts the expected amount of parameters.
    
    Parameters
    ----------
    exception_handler : `CoroutineFunctionType`
        A function, which handles an exception and returns whether handled it.
        
        The following parameters are passed to it:
        
        +-------------------+-------------------------------------------------------------------------------+
        | Name              | Type                                                                          |
        +===================+===============================================================================+
        | client            | ``Client``                                                                    |
        +-------------------+-------------------------------------------------------------------------------+
        | interaction_event | ``InteractionEvent``                                                          |
        +-------------------+-------------------------------------------------------------------------------+
        | command           | ``ComponentCommand``, ``SlashCommand``,                                       |
        |                   | ``SlashCommandFunction``, ``SlashCommandCategory``,                           |
        |                   | ``SlashCommandParameterAutoCompleter``                                        |
        +-------------------+-------------------------------------------------------------------------------+
        | exception         | `BaseException`                                                               |
        +-------------------+-------------------------------------------------------------------------------+
        
        Should return the following parameters:
        
        +-------------------+-----------+
        | Name              | Type      |
        +===================+===========+
        | handled           | `bool`    |
        +-------------------+-----------+
    
    Raises
    ------
    TypeError
        - If `exception_handler` accepts bad amount of parameters.
        - If `exception_handler` is not a coroutine function.
    """
    analyzer = CallableAnalyzer(exception_handler)
    if not analyzer.is_async():
        raise TypeError(
            f'`exception_handler` can be `async` function, got {exception_handler!r}.'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 4:
        raise TypeError(
            f'`exception_handler` should accept `4` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got {exception_handler!r}.'
        )
    
    if min_ != 4:
        if max_ < 4:
            if not analyzer.accepts_args():
                raise TypeError(
                    f'`exception_handler` should accept `4` parameters, meanwhile the given callable '
                    f'expects up to `{max_!r}`, got {exception_handler!r}.'
                )


def _register_exception_handler(parent, first, exception_handler):
    """
    Registers an exception handler to the respective entity. This function is wrapped inside of
    `functools.partial` with it's `parent` and `first` parameters.
    
    Parameters
    ----------
    parent : ``Slasher``, ``SlashCommand`, ``SlashCommandCategory``, ``ComponentCommand``,
            ``SlashCommandFunction``, ``SlashCommandParameterAutoCompleter``
        The slasher to register the exception handler to.
    first : `bool`
        Whether the exception handler should run first.
    exception_handler : `CoroutineFunctionType`
        Exception handler to register.
    
    Returns
    -------
    exception_handler : `CoroutineFunctionType`
    
    Raises
    ------
    RuntimeError
        If `exception_handler` is given as `None`.
    """
    if (exception_handler is None):
        raise RuntimeError('`exception_handler` cannot be `None`.')
    
    return parent._register_exception_handler(exception_handler, first)


class ExceptionHandlerInterface(RichAttributeErrorBaseType):
    """
    Common class for exception handleable objects.
    """
    __slots__ = ()
    
    def error(self, exception_handler = None, *, first = False):
        """
        Registers an exception handler to the ``SlashCommandCategory``.
        
        Parameters
        ----------
        exception_handler : `None`, `CoroutineFunctionType` = `None`, Optional
            Exception handler to register.
        first : `bool` = `False`, Optional (Keyword Only)
            Whether the exception handler should run first.
        
        Returns
        -------
        exception_handler / wrapper : `CoroutineFunctionType` / `functools.partial`
            If `exception_handler` is not given, returns a wrapper.
        """
        if exception_handler is None:
            return partial_func(_register_exception_handler, first)
        
        return self._register_exception_handler(exception_handler, first)
    
    
    def _register_exception_handler(self, exception_handler, first):
        """
        Registers an exception handler to the ``SlashCommandCategory``.
        
        Parameters
        ----------
        exception_handler : `CoroutineFunctionType`
            Exception handler to register.
        first : `bool`
            Whether the exception handler should run first.
        
        Returns
        -------
        exception_handler : `CoroutineFunctionType`
        """
        test_exception_handler(exception_handler)
        self._store_exception_handler(exception_handler, first)
        return exception_handler
    
    
    def _store_exception_handler(self, exception_handler, first):
        """
        Stores the exception handler.
        
        Parameters
        ----------
        exception_handler : `CoroutineFunctionType`
            Exception handler to register.
        first : `bool`
            Whether the exception handler should run first.
        
        Returns
        -------
        stored : `bool`
        instance : `CoroutineFunctionType`
        """
        exception_handlers = self._exception_handlers
        if exception_handlers is None:
            exception_handlers = []
            self._exception_handlers = exception_handlers
        
        if first:
            exception_handlers.insert(0, exception_handler)
        else:
            exception_handlers.append(exception_handler)
        return True, exception_handler
    
    
    @property
    def _exception_handlers(self):
        """
        The registered exception handlers.
        
        Overwrite it as an attribute in subclasses.
        
        Returns
        -------
        _exception_handlers : `None | list<CoroutineFunctionType>`
        """
        return None
    
    
    @_exception_handlers.setter
    def _exception_handlers(self, value):
        pass
