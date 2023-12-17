__all__ = ('CommandBase',)

from warnings import warn

from scarletio import RichAttributeErrorBaseType

from .....discord.events.handling_helpers import create_event_from_class

from ...interfaces.exception_handler import ExceptionHandlerInterface


class CommandBase(ExceptionHandlerInterface, RichAttributeErrorBaseType):
    """
    Base type for ``Slasher``'s commands.
    
    Attributes
    ----------
    _exception_handlers : `None`, `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _parent_reference : `None`, ``WeakReferer`` to ``SlashCommand``
        The parent slasher of the component command.

    name : `str`
        The command's name.
        
        Only used for debugging.
    
    Class Attributes
    ----------------
    COMMAND_COMMAND_NAME : `str`
        The command's name defining parameter's name.
    COMMAND_PARAMETER_NAMES : `tuple` of `str`
        All parameters names accepted by ``.__new__``
    COMMAND_NAME_NAME : `str`
        The command's "command" defining parameter's name.
    """
    __slots__ = ('name', '_exception_handlers', '_parent_reference',)

    COMMAND_NAME_NAME = 'name'
    COMMAND_COMMAND_NAME = 'command'
    
    COMMAND_PARAMETER_NAMES = (
        COMMAND_NAME_NAME,
        COMMAND_COMMAND_NAME,
        'allowed_mentions',
        'wait_for_acknowledgement',
        'show_for_invoking_user_only',
    )
    
    
    @classmethod
    def from_class(cls, klass):
        """
        Creates a new command instance from the given `klass`.
        
        Parameters
        ----------
        klass : `type`
            The class to create custom id based command from.
        
        Returns
        -------
        self : ``CommandBase``, ``Router``
        
        Raises
        ------
        TypeError
            If any attribute's type is incorrect.
        ValueError
            If any attribute's value is incorrect.
        """
        warn(
            (
                f'Creating commands with the from class constructor is deprecated and will be removed in 2024 Jun. '
                f'Please use command decorators instead.'
            ),
            FutureWarning,
            stacklevel = 5,
        )
        
        return create_event_from_class(
            cls, klass, cls.COMMAND_PARAMETER_NAMES, cls.COMMAND_NAME_NAME, cls.COMMAND_COMMAND_NAME
        )


    def __new__(cls, func, name = None, **keyword_parameters):
        """
        Creates a new custom_id based command instance.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        func : `None`, `async-callable`
            The function used as the command when using the respective slash command.
        name : `None`, `str` = `None`, Optional
            The name of the component command.

        Returns
        -------
        self : ``CommandBase``, ``Router``
        
        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError
    
    
    def _build_repr_body_into(self, repr_parts):
        """
        Representation builder helper to build the representation's body.
        """
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
    
    
    def __repr__(self):
        """Returns the command's representation."""
        repr_parts = ['<', self.__class__.__name__]
        self._build_repr_body_into(repr_parts)
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __format__(self, code):
        """Formats the command in a format string."""
        if not code:
            return str(self)
        
        if code == 'm':
            return self.mention
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
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
    
    
    def __eq__(self, other):
        """Returns whether the two commands are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
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
        guild : ``Guild``, `int`
            The guild to get the command's mention.
        
        Returns
        -------
        mention : `str`
        """
        return ''
