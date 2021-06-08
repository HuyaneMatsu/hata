__all__ = ('SlashCommandError',)

class SlashCommandError(Exception):
    """
    Base class for slash command internal errors.
    """
    pass


class SlashCommandParameterConversionError(SlashCommandError):
    """
    Exception raised when a command's parameter's parsing fails.
    
    Attributes
    ----------
    _repr : `None` or `str`
        The generated error message.
    parameter_name : `str` or `None`
        The parameter's name, which failed to be parsed.
    received_value : `str` or `None`
        The parameter's received value.
    excepted_type : `str` or `None`
        The parameter's expected type's name.
    expected_values : `None` or `list` of `Any`
        Expected values.
    """
    def __init__(self, parameter_name, received_value, excepted_type, expected_values):
        """
        Creates a new ``SlashCommandParameterConversionError`` instance with the given parameters.
        
        Parameters
        ----------
        parameter_name : `str` or `None`
            The parameter's name, which failed to be parsed.
        received_value : `str` or `None`
            The parameter's received value.
        excepted_type : `str` or `None`
            The parameter's expected type's name.
        expected_values : `None` or `list` of `Any`
            Expected values.
        """
        self.parameter_name = parameter_name
        self.received_value = received_value
        self.excepted_type = excepted_type
        self.expected_values = expected_values
        self._repr = None
        Exception.__init__(self, parameter_name, received_value, excepted_type, expected_values)
    
    def __repr__(self):
        """Returns the representation of the parameter conversion error."""
        repr_ = self._repr
        if repr_ is None:
            repr_ = self._create_repr()
        
        return repr_

    def _create_repr(self):
        """
        Creates the representation of the parsing syntax error.
        
        Returns
        -------
        repr_ : `str`
            The representation of the syntax error.
        """
        repr_parts = [self.__class__.__name__]
        
        parameter_name = self.parameter_name
        if (parameter_name is not None):
            repr_parts.append('\n')
            repr_parts.append('parameter name: ')
            repr_parts.append(repr(parameter_name))
        
        repr_parts.append(
            '\n'
            'received value: '
        )
        received_value = self.received_value
        if (received_value is None):
            repr_parts.append('N/A')
        else:
            repr_parts.append(repr(received_value))
        
        excepted_type = self.excepted_type
        if (excepted_type is not None):
            repr_parts.append(
                '\n'
                'expected type: '
            )
            repr_parts.append(excepted_type)
        
        expected_values = self.expected_values
        if (expected_values is not None):
            repr_parts.append(
                '\n'
                'expected value(s):'
            )
            
            index = 0
            limit = len(expected_values)
            while True:
                value = expected_values[index]
                index += 1
                
                repr_parts.append(repr(value))
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
        
        repr_ = ''.join(repr_parts)
        self._repr = repr_
        return repr_
