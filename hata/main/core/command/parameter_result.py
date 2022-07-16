__all__ = ('ParameterResult',)

from scarletio import RichAttributeErrorBaseType

from .result import COMMAND_RESULT_CODE_CONVERSION_FAILED, CommandResult


class ParameterResult(RichAttributeErrorBaseType):
    """
    Attributes
    ----------
    command_parameter : ``CommandParameter``
        The represented command parameter.
    fed_items : `None`, `list` of `tuple` (`str`, `Any`) items
        Fed values to the parameter as results.
    """
    __slots__ = ('command_parameter', 'fed_items',)
    
    def __new__(cls, command_parameter):
        """
        Creates a new parameter result instance.
        
        Parameters
        ----------
        command_parameter : ``CommandParameter``
            The represented command parameter.
        """
        self = object.__new__(cls)
        self.command_parameter = command_parameter
        self.fed_items = None
        return self
    
    
    def is_satisfiable(self):
        """
        Returns whether the parameter can be satisfied.
        
        Returns
        -------
        is_satisfiable : `bool`
        """
        if self.fed_items is None:
            return True
        
        parameter = self.command_parameter.parameter
        if parameter.is_args() or parameter.is_kwargs():
            return True
        
        return False
    
    
    def is_satisfied(self):
        """
        Returns whether the parameter is satisfied.
        
        Returns
        -------
        is_satisfied : `bool`
        """
        if (self.fed_items is not None):
            return True
        
        parameter = self.command_parameter.parameter
        if parameter.has_default:
            return True
        
        if parameter.is_args() or parameter.is_kwargs():
            return True
        
        return False
    
    
    def feed(self, value):
        """
        Feeds a value with the given name.
        
        Parameters
        ----------
        value : `Any`
            The value to feed.
        
        Returns
        ------
        command_result : `None`, ``CommandResult``
        """
        return self._feed(value, self.command_parameter.parameter.name)
    
    
    def feed_as(self, value, name):
        """
        Feeds a value with the given name.
        
        Parameters
        ----------
        value : `Any`
            The value to feed.
        name : `str`
            The value's name.
        
        Returns
        ------
        command_result : `None`, ``CommandResult``
        """
        name = name.replace('-', '_')
        return self._feed(value, name)
    
    
    def _feed(self, value, name):
        """
        Feeds a value with the given name.
        
        This method is either called by ``.feed`` after auto filling `name`. Or by ``.feed_as`` after normalising
        the name.
        
        Parameters
        ----------
        value : `Any`
            The value to feed.
        name : `str`
            The value's name.
        
        Returns
        ------
        command_result : `None`, ``CommandResult``
        """
        converter = self.command_parameter.get_converter()
        converted_value = converter(value)
        
        if (converted_value is None):
            return CommandResult(
                COMMAND_RESULT_CODE_CONVERSION_FAILED,
                self.command_parameter,
                value,
            )
        
        
        fed_items = self.fed_items
        if (fed_items is None):
            fed_items = []
            self.fed_items = fed_items
        
        fed_items.append((name, converted_value))
        return None
    
    
    def matches_name(self, name):
        """
        Returns whether the parameter matches the given name.
        
        Parameters
        ----------
        name : `str`
            The name to match.
        
        Returns
        -------
        is_matching : `bool`
        """
        command_parameter = self.command_parameter
        if command_parameter.display_name == name:
            return True
        
        if self.command_parameter.parameter.is_kwargs():
            return True
        
        return False
    
    
    def is_modifier(self):
        """
        Returns whether the parameter is a modifier parameter.
        
        Returns
        -------
        is_modifier : `str`
        """
        return self.command_parameter.is_modifier()
    
    
    
    def is_positional(self):
        """
        Returns whether the parameter is a positional parameter.
        
        Returns
        -------
        is_positional : `bool`
        """
        parameter = self.command_parameter.parameter
        if parameter.is_positional() or parameter.is_args():
            return True
        
        return False
    
    
    def has_fed_items(self):
        """
        Returns whether the parameter has fed values.
        
        Returns
        -------
        has_fed_items : `bool`
        """
        return (self.fed_items is not None)
    
    
    def get_fed_value(self):
        """
        Returns the first fed value.
        
        Returns
        -------
        value : `None`, `Any`
        """
        fed_items = self.fed_items
        if (fed_items is not None):
            return fed_items[0][1]
    
    
    def get_fed_item(self):
        """
        Returns the first fed item.
        
        Returns
        -------
        item : `None`, `tuple` (`str`, `Any`) item
        """
        fed_items = self.fed_items
        if (fed_items is not None):
            return fed_items[0]
    
    
    def iter_fed_values(self):
        """
        Iterates over the fed values of the parameter result.
        
        This method is an iterable generator.
        
        Yields
        ------
        value : `Any`
        """
        fed_items = self.fed_items
        if (fed_items is not None):
            for fed_item in fed_items:
                yield fed_item[1]
    
    
    def iter_fed_items(self):
        """
        Iterates over the fed items of the parameter result.
        
        This method is an iterable generator.
        
        Yields
        ------
        item : `tuple` (`str`, `Any`)
        """
        fed_items = self.fed_items
        if (fed_items is not None):
            yield from fed_items
    
    
    def put_into(self, positional_parameters, keyword_parameters):
        """
        Puts the value of the parameter into the given containers representing a function's call parameters.
        
        Parameters
        ----------
        positional_parameters : `list` of `Any`
            Positional parameters to call the respective function with.
        keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters to call the respective function with.
        
        Returns
        -------
        was_put : `bool`
            Whether putting values into the parameters was successful.
        """
        parameter = self.command_parameter.parameter
        if parameter.is_positional():
            if self.has_fed_items():
                positional_parameters.append(self.get_fed_value())
                return True
            
            if parameter.has_default:
                positional_parameters.append(parameter.default)
                return True
            
            return False
        
        
        if parameter.is_keyword_only():
            if self.has_fed_items():
                key, value = self.get_fed_item()
                keyword_parameters[key] = value
                return True
            
            if parameter.has_default:
                keyword_parameters[parameter.name] = parameter.default
                return True
            
            return False
        
        
        if parameter.is_args():
            positional_parameters.extend(self.iter_fed_values())
            return True
        
        
        if parameter.is_kwargs():
            keyword_parameters.update(self.iter_fed_items())
            return True
        
        
        return False
