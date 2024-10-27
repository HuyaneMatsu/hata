__all__ = ('CommandBase',)

from scarletio import RichAttributeErrorBaseType

from ...interfaces.exception_handler import ExceptionHandlerInterface


class CommandBase(ExceptionHandlerInterface, RichAttributeErrorBaseType):
    """
    Base type for ``Slasher``'s commands.
    
    Attributes
    ----------
    _exception_handlers : `None | list<CoroutineFunction>`
        Exception handlers added with ``.error`` to the interaction handler.
        
    _parent_reference : `None | WeakReferer<SelfReferenceInterface>`
        The parent slasher of the component command.

    name : `str`
        The command's name.
        
        Only used for debugging.
    """
    __slots__ = ('_exception_handlers', '_parent_reference', 'name')
    
    
    def __new__(cls, function, name = None, **keyword_parameters):
        """
        Creates a new command instance.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        function : `None | async-callable`
            The function used as the command when using the respective slash command.
        
        name : `None | str` = `None`, Optional
            The name of the component command.
        
        **keyword_parameters : Keyword Parameters
            Additional Keyword parameters.
        
        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError
    
    
    def __repr__(self):
        """Returns the command's representation."""
        repr_parts = ['<', type(self).__name__]
        repr_parts = self._put_repr_parts_into(repr_parts)
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _put_repr_parts_into(self, repr_parts):
        """
        Representation builder helper to build the representation's body.
        
        Parameters
        ----------
        repr_parts : `list<str>`
            Parts to extend.
        
        Returns
        -------
        repr_parts : `list<str>`
        """
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        exception_handlers = self._exception_handlers
        if (exception_handlers is not None):
            repr_parts.append(', exception_handlers = ')
            repr_parts.append(repr(exception_handlers))
        
        return repr_parts
    
    
    def __hash__(self):
        """Returns the command's hash value."""
        hash_value = 0
        
        # _exception_handlers
        exception_handlers = self._exception_handlers
        if (exception_handlers is not None):
            hash_value ^= len(exception_handlers) << 4
            
            for exception_handler in exception_handlers:
                try:
                    exception_handler_hash_value = hash(exception_handler)
                except TypeError:
                    exception_handler_hash_value = object.__hash__(exception_handler)
                hash_value ^= exception_handler_hash_value
        
        # _parent_reference
        # Internal field
        
        # name
        hash_value ^= hash(self.name)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two commands are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two types are equal.
        
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        # _exception_handlers
        if self._exception_handlers != other._exception_handlers:
            return False
        
        # _parent_reference
        # Internal field
        
        # name
        if self.name != other.name:
            return False
        
        return True
    
    
    def __format__(self, code):
        """Formats the command in a format string."""
        if not code:
            return str(self)
        
        if code == 'm':
            return self.mention
        
        raise ValueError(
            f'Unknown format code {code!r} for {type(self).__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"m"!r}.'
        )
    
    
    async def invoke(self, client, interaction_event):
        """
        Calls the command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        return
    
    
    def copy(self):
        """
        Copies the command.
        
        Returns
        -------
        new : `type<self>`
        """
        new = object.__new__(type(self))
        
        # _exception_handlers
        exception_handlers = self._exception_handlers
        if (exception_handlers is not None):
            exception_handlers = exception_handlers.copy()
        new._exception_handlers = exception_handlers
        
        # _parent_reference
        new._parent_reference = None
        
        # name
        new.name = self.name
        
        return new
    
    
    # ---- Mention ----
    
    @property
    def mention(self):
        """
        Returns the command mention.
        Applicable for slash and context commands.
        
        Returns
        -------
        mention : `str`
        """
        return ''
    
    
    def mention_at(self, guild):
        """
        Mentions the command at the specified guild.
        Should be used when the command is added to multiple guilds.
        Applicable for slash and context commands.
        
        Parameters
        ----------
        guild : `Guild | int`
            The guild to get the command's mention.
        
        Returns
        -------
        mention : `str`
        """
        return ''
