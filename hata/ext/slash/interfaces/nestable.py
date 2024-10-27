__all__ = ()

from scarletio import RichAttributeErrorBaseType

from ....discord.events.handling_helpers import _EventHandlerManager, Router


class NestableInterface(RichAttributeErrorBaseType):
    """
    Common class for nestable instances.
    """
    __slots__ = ()
    
    
    def _is_nestable(self):
        """
        Returns whether the instance can be nested.
        
        Returns
        -------
        nestable : `bool`.
        """
        return True
    
    
    def _check_supports_nesting(self):
        """
        If the instance is not nestable raises `RuntimeError`.
        
        Raises
        ------
        RuntimeError
            The instance is not nestable.
        """
        if not self._is_nestable():
            raise RuntimeError(f'{self!r} is not nestable.')
    
    
    @property
    def interactions(self):
        """
        Enables you to add sub-commands or sub-categories to the command.
        
        Raises
        ------
        RuntimeError
            The instance is not nestable.
        """
        self._check_supports_nesting()
        return _EventHandlerManager(self)
    
    
    def create_event(self, function, *positional_parameters, **keyword_parameters):
        """
        Adds a sub-command under the slash command.
        
        Parameters
        ----------
        func : `async-callable`
            The function used as the command when using the respective slash command.
        
        *positional_parameters : Positional Parameters
            Positional parameters to pass to ``SlashCommand``'s constructor.
        
        **keyword_parameters : Keyword parameters
            Keyword parameters to pass to the ``SlashCommand``'s constructor.
        
        Returns
        -------
        instance : `object`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        RuntimeError
            - If cant register sub-command.
        """
        self._check_supports_nesting()
        
        if isinstance(function, Router):
            function = function[0]
        
        added, instance = self._store_command_instance(function)
        if added:
            return instance
        
        command = self._make_command_instance_from_parameters(function, positional_parameters, keyword_parameters)
        
        added, instance = self._store_command_instance(command)
        if added:
            return instance
        
        return command
    
    
    def _make_command_instance_from_parameters(self, function, positional_parameters, keyword_parameters):
        """
        Creates a command instance from the given parameters.
        
        Parameters
        ----------
        function : `None | CoroutineFunctionType | CoroutineGeneratorFunctionType`
            Function to create command from.
        positional_parameters : `tuple<object>`
            Captured positional parameters.
        keyword_parameters : `dict<str, object>`
            Captured keyword parameters.
        
        Returns
        -------
        instance : `object`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        RuntimeError
            - If cant register sub-command.
        """
        return None
    
    
    def _store_command_instance(self, command):
        """
        Registers a nestable instance.
        
        Parameters
        ----------
        command : `object`
            Command instance to register.
        
        Returns
        -------
        registered : `bool`
        instance : `None | object`
        """
        return False, None
