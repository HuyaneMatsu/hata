__all__ = ()


from scarletio import RichAttributeErrorBaseType


class CommandInterface(RichAttributeErrorBaseType):
    """
    Common class for command objects.
    """
    __slots__ = ()
    
    def get_command_function(self):
        """
        Returns the command function of the instance.
        
        Returns
        -------
        command_function : `None | CoroutineFunctionType | CoroutineGeneratorFunctionType`
        """
        return None
