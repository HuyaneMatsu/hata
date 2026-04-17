__all__ = ()

from scarletio import CauseGroup, copy_docs

from ...discord.events.handling_helpers import Router

from .interfaces.autocomplete import AutocompleteInterface
from .interfaces.exception_handler import ExceptionHandlerInterface
from .interfaces.nestable import NestableInterface


class InteractionCommandRouter(AutocompleteInterface, ExceptionHandlerInterface, NestableInterface, Router):
    """
    Router for returned grouped interactions.
    """
    __slots__ = ()
    
    # ---- AutocompleteInterface ----
    
    def _check_supports_auto_completion(self):
        for instance in self:
            if not isinstance(instance, AutocompleteInterface):
                raise RuntimeError(
                    f'At least 1 instance of the router does not supports auto completion; got {instance!r}.'
                )
    
    
    @copy_docs(AutocompleteInterface.autocomplete)
    def autocomplete(self, parameter_name, *parameter_names, function = ...):
        self._check_supports_auto_completion()
        return AutocompleteInterface.autocomplete(self, parameter_name, *parameter_names, function = function)
    
    
    @copy_docs(AutocompleteInterface._register_auto_completer)
    def _register_auto_completer(self, function, parameter_names):
        self._check_supports_auto_completion()

        exceptions = None
        added_auto_completers = []
        
        for instance in self:
            try:
                added_auto_completer = instance._register_auto_completer(function, parameter_names)
            except RuntimeError as exception:
                if exceptions is None:
                    exceptions = []
                
                exceptions.append(exception)
            
            else:
                added_auto_completers.append(added_auto_completer)
        
        
        if exceptions is not None:
            raise RuntimeError(
                'One or more exception occurred while registering autocompleter.'
            ) from CauseGroup(*exceptions)
        
        
        return type(self)(added_auto_completers)
    
    
    # ---- ExceptionHandlerInterface ----
    
    def _check_supports_exception_handler(self):
        for instance in self:
            if not isinstance(instance, ExceptionHandlerInterface):
                raise RuntimeError(
                    f'At least 1 instance of the router does not supports exception handlers; got {instance!r}.'
                )
    
    
    @copy_docs(ExceptionHandlerInterface.error)
    def error(self, exception_handler = None, *, first = False):
        self._check_supports_exception_handler()
        return ExceptionHandlerInterface.error(exception_handler, first = False)
    
    
    @copy_docs(ExceptionHandlerInterface._register_exception_handler)
    def _register_exception_handler(self, exception_handler, first):
        self._check_supports_exception_handler()
        
        exceptions = None
        
        for instance in self:
            try:
                instance._register_exception_handler(exception_handler, first)
            except RuntimeError as exception:
                if exceptions is None:
                    exceptions = []
                
                exceptions.append(exception)
        
        
        if exceptions is not None:
            raise RuntimeError(
                'One or more exception occurred while registering exception handler.'
            ) from CauseGroup(*exceptions)
        
        
        return exception_handler
    
    
    # ---- NestableInterface ----
    
    
    @copy_docs(NestableInterface._is_nestable)
    def _is_nestable(self):
        for instance in self:
            if (not isinstance(instance, NestableInterface)) or (not instance._is_nestable()):
                return False
        
        return True
    
    
    @copy_docs(NestableInterface._check_supports_nesting)
    def _check_supports_nesting(self):
        for instance in self:
            if (not isinstance(instance, NestableInterface)) or (not instance._is_nestable()):
                raise RuntimeError(
                    f'At least 1 instance of the router does not supports nesting; got {instance!r}.'
                )
    
    
    @copy_docs(NestableInterface.create_event)
    def create_event(self, function, *positional_parameters, **keyword_parameters):
        self._check_supports_nesting()
        
        exceptions = None
        commands = []
        
        for instance in self:
            try:
                command = instance.create_event(function, *positional_parameters, **keyword_parameters)
            except RuntimeError as exception:
                if exceptions is None:
                    exceptions = []
                
                exceptions.append(exception)
            
            else:
                commands.append(command)
        
        
        if exceptions is not None:
            raise RuntimeError(
                'One or more exception occurred while nesting.'
            ) from CauseGroup(*exceptions)
        
        
        return type(self)(commands)
