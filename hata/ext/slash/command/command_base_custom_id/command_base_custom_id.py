__all__ = ('CommandBaseCustomId', )

from scarletio import copy_docs

from ..command_base import CommandBase


class CommandBaseCustomId(CommandBase):
    """
    Base type for commands based on `custom_id` matching.
    
    Attributes
    ----------
    _exception_handlers : `None`, `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _parent_reference : `None`, ``WeakReferer`` to ``SlashCommand``
        The parent slasher of the component command.
    _parameter_converters : `tuple` of ``ParameterConverter``
        Parsers to parse command parameters.
    _command_function : `async-callable˛
        The command's function to call.
    _string_custom_ids : `None`, `tuple` of `str`
        The custom id-s to wait for.
    _regex_custom_ids : `None`, `tuple` of `re.Pattern`.
        Regex pattern to match custom-ids.
    name : `str`
        The command's name.
        
        Only used for debugging.
    
    response_modifier : `None`, ``ResponseModifier``
        Modifies values returned and yielded to command coroutine processor.
    
    Class Attributes
    ----------------
    COMMAND_COMMAND_NAME : `str`
        The command's name defining parameter's name.
    COMMAND_PARAMETER_NAMES : tuple of `str`
        All parameters names accepted by ``.__new__``
    COMMAND_NAME_NAME : `str`
        The command's "command" defining parameter's name.
    """
    __slots__ = (
        '_command_function', '_parameter_converters', '_regex_custom_ids', '_string_custom_ids', 'response_modifier',
    )
    
    COMMAND_PARAMETER_NAMES = (
        *CommandBase.COMMAND_PARAMETER_NAMES,
        'custom_id',
    )
    
    
    def __new__(cls, func, custom_id, name=None, **keyword_parameters):
        """
        Creates a new custom_id based command instance.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        func : `None`, `async-callable`
            The function used as the command when using the respective slash command.
        custom_id : `str`, (`list`, `set`) of `str`, `tuple` of (`str`, (`list`, `set`) of `str`)
            Custom id to match by the component command.
        name : `None`, `str` = `None`, Optional
            The name of the component command.
        **keyword_parameters : Keyword parameters
            Additional keyword parameters
        
        Other parameters
        ----------------
        allowed_mentions : `None`, `str`, ``UserBase``, ``Role``, ``AllowedMentionProxy``, \
                `list` of (`str`, ``UserBase``, ``Role`` ), Optional (Keyword only)
            Which user or role can the response message ping (or everyone).
        show_for_invoking_user_only : `bool`, Optional (Keyword only)
            Whether the response message should only be shown for the invoking user.
        wait_for_acknowledgement : `bool`, Optional (Keyword only)
            Whether acknowledge tasks should be ensure asynchronously.
        
        Returns
        -------
        self : ``CommandBaseCustomId``, ``Router``
        
        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError
    
    
    @copy_docs(CommandBase._cursed_repr_builder)
    def _cursed_repr_builder(self):
        for repr_parts in CommandBase._cursed_repr_builder(self):
            
            string_custom_ids = self._string_custom_ids
            if (string_custom_ids is not None):
                
                repr_parts.append(', string_custom_ids=[')
                index = 0
                limit = len(string_custom_ids)
                
                while True:
                    string_custom_id = string_custom_ids[index]
                    repr_parts.append(repr(string_custom_id))
                    
                    index += 1
                    if index == limit:
                        break
                    
                    repr_parts.append(', ')
                    continue
                
                repr_parts.append(']')
            
            regex_custom_ids = self._regex_custom_ids
            if (regex_custom_ids is not None):
                
                repr_parts.append(', regex_custom_ids=[')
                index = 0
                limit = len(regex_custom_ids)
                
                while True:
                    regex_custom_id = regex_custom_ids[index]
                    repr_parts.append(repr(regex_custom_id.pattern.pattern))
                    
                    index += 1
                    if index == limit:
                        break
                    
                    repr_parts.append(', ')
                    continue
                
                repr_parts.append(']')
            
            
            yield repr_parts
            
            response_modifier = self.response_modifier
            if (response_modifier is not None):
                repr_parts.append(', response_modifier=')
                repr_parts.append(repr(response_modifier))
    
    
    async def invoke(self, client, interaction_event, regex_match):
        """
        Calls the command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        regex_match : `None`, ``RegexMatch``
            The matched regex if applicable.
        """
        return
    
    
    @copy_docs(CommandBase.__hash__)
    def __hash__(self):
        hash_value = CommandBase.__hash__(self)
        
        # _command_function
        command_function = self._command_function
        try:
            command_function_hash_value = hash(command_function)
        except KeyError:
            command_function_hash_value = object.__hash__(command_function)
        hash_value ^= command_function_hash_value
        
        # _parameter_converters
        # Internal field
        
        # _regex_custom_ids
        regex_custom_ids = self._regex_custom_ids
        if (regex_custom_ids is not None):
            hash_value ^= hash(regex_custom_ids)
        
        # _string_custom_ids
        string_custom_ids = self._string_custom_ids
        if (string_custom_ids is not None):
            hash_value ^= hash(string_custom_ids)
        
        # response_modifier
        response_modifier = self.response_modifier
        if (response_modifier is not None):
            hash_value ^= hash(response_modifier)
        
        return hash_value
    
    
    @copy_docs(CommandBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not CommandBase._is_equal_same_type(self, other):
            return False
        
        # _command_function
        if self._command_function != other._command_function:
            return False
        
        # _parameter_converters
        # Internal field
        
        # _regex_custom_ids
        if self._regex_custom_ids != other._regex_custom_ids:
            return False
        
        # _string_custom_ids
        if self._string_custom_ids != other._string_custom_ids:
            return False
        
        # response_modifier
        if self.response_modifier != other.response_modifier:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the command.
        
        Returns
        -------
        new : ``CommandBaseCustomId``
        """
        new = CommandBase.copy(self)
        
        # _command_function
        new._command_function = self._command_function
        
        # _parameter_converters
        new._parameter_converters = self._parameter_converters
        
        # _regex_custom_ids
        new._regex_custom_ids = self._regex_custom_ids
        
        # _string_custom_ids
        new._string_custom_ids = self._string_custom_ids
        
        # response_modifier
        new.response_modifier = self.response_modifier
        
        return new
