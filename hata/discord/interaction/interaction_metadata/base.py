__all__ = ('InteractionMetadataBase',)

from scarletio import RichAttributeErrorBaseType, copy_docs

from ...bases import PlaceHolder
from ...component import ComponentType

from ..resolved import Resolved

ENTITY_RESOLVERS = {
    ComponentType.user_select: (lambda resolved, entity_id: resolved.resolve_user(entity_id)),
    ComponentType.role_select: (lambda resolved, entity_id: resolved.resolve_role(entity_id)),
    ComponentType.mentionable_select: (lambda resolved, entity_id: resolved.resolve_mentionable(entity_id)),
    ComponentType.channel_select: (lambda resolved, entity_id: resolved.resolve_channel(entity_id)),
}


class InteractionMetadataBase(RichAttributeErrorBaseType):
    """
    Base class for values assigned to ``InteractionEvent.interaction`` field.
    """
    __slots__ = ()
    
    def __new__(cls, **keyword_parameters):
        """
        Creates a new interaction metadata from the given parameters.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            Keyword parameters defining how should the fields be set.
        
        Other Parameters
        ----------------
        component_type : ``ComponentType``, Optional (Keyword only)
            The used component's type.
        
        components : `None`, `tuple` of ``InteractionComponent``, Optional (Keyword only)
            Submitted component values of a form submit interaction.
        
        custom_id : `None`, `str`, Optional (Keyword only)
            Component or form interaction's custom identifier.
        
        id : `int`, Optional (Keyword only)
            The represented application command's identifier number.
        
        name : `str`, Optional (Keyword only)
            The represented application command's name.
        
        options : `None`, `tuple` of ``InteractionOption``, Optional (Keyword only)
            Application command option representations. Like sub-command or parameter.
        
        resolved : `None`, ``Resolved``, Optional (Keyword only)
            Contains the received entities.
        
        target_id : `int`, Optional (Keyword only)
            The interaction's target's identifier. Applicable for context commands.
        
        values : `None`, `tuple` of `str`, Optional (Keyword only)
            Values selected by the user. Applicable for component interactions.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra or unused parameters.
        ValueError
            - If a field's value is incorrect.
        """
        self = cls._create_empty()
        if keyword_parameters:
            self._set_attributes_from_keyword_parameters(keyword_parameters)
        return self
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates an new interaction with it's attribute set as it's default values.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)    
    
    
    def copy(self):
        """
        Copies the integration option.
        
        Returns
        -------
        new : `instance<cls>`
        """
        return object.__new__(type(self))
    
    
    def copy_with(self, **keyword_parameters):
        """
        Copies the integration with replacing the defined fields.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            Keyword parameters defining which fields and how should be set.
        
        Other Parameters
        ----------------
        component_type : ``ComponentType``, Optional (Keyword only)
            The used component's type.
        
        components : `None`, `tuple` of ``InteractionComponent``, Optional (Keyword only)
            Submitted component values of a form submit interaction.
        
        custom_id : `None`, `str`, Optional (Keyword only)
            Component or form interaction's custom identifier.
        
        id : `int`, Optional (Keyword only)
            The represented application command's identifier number.
        
        name : `str`, Optional (Keyword only)
            The represented application command's name.
        
        options : `None`, `tuple` of ``InteractionOption``, Optional (Keyword only)
            Application command option representations. Like sub-command or parameter.
        
        resolved : `None`, ``Resolved``, Optional (Keyword only)
            Contains the received entities.
        
        target_id : `int`, Optional (Keyword only)
            The interaction's target's identifier. Applicable for context commands.
        
        values : `None`, `tuple` of `str`, Optional (Keyword only)
            Values selected by the user. Applicable for component interactions.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
            - Extra or unused fields given.
        ValueError
            - If a field's value is incorrect.
        """
        self = self.copy()
        if keyword_parameters:
            self._set_attributes_from_keyword_parameters(keyword_parameters)
        return self
    
    
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        """
        Sets the integration's attributes from the given keyword parameters.
        
        Parameters
        keyword_parameters : Keyword parameters
            A dictionary of keyword parameters defining which fields and how should be set.
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
            - Extra or unused fields given.
        ValueError
            - If a field's value is incorrect.
        """
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused keyword parameters: {keyword_parameters!r}.'
            )
    
    
    @classmethod
    def from_data(cls, data, interaction_event):
        """
        Creates a new interaction from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received interaction field data.
        
        interaction_event : ``InteractionEvent``
            The parent interaction event.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    def to_data(cls, *, defaults = False, interaction_event = None):
        """
        Converts the interaction into a json serailzable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included as well.
        
        interaction_event : ``InteractionEvent`` = `None`, Optional (Keyword only)
            The respective guild's identifier to use for handing user guild profiles.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def __repr__(self):
        """Returns the interaction's representation."""
        repr_parts = []
        repr_parts.append('<')
        repr_parts.append(self.__class__.__name__)
        
        self._put_attribute_representations_into(repr_parts)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _put_attribute_representations_into(self, repr_parts):
        """
        Helper function to build representation of the interaction metadata.
        
        Parameters
        ----------
        repr_parts : `list` of `str`
            Integration metadata representation parts.
        
        Returns
        -------
        field_added : `bool`
            Whether any field was added.
        """
        return False
    
    
    def __hash__(self):
        """Returns the interaction's hash value."""
        return 0
    
    
    def __eq__(self, other):
        """Returns whether the two interactions are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two interactions are equal.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other interaction. Must be the same type as `self`.
        
        Returns
        -------
        is_equal : `bool`
        """
        return True
    
    
    component_type = PlaceHolder(
        ComponentType.none,
        """
        The used component's type.
        
        Returns
        -------
        component_type : ``ComponentType``
        """
    )
    
    
    components = PlaceHolder(
        None,
        """
        Submitted component values of a form submit interaction.
        
        Returns
        -------
        components : `None`, `tuple` of ``InteractionComponent``
        """
    )
    
    
    custom_id = PlaceHolder(
        None,
        """
        Component or form interaction's custom identifier.
        
        Returns
        -------
        custom_id : `None`, `str`
        """,
    )
    
    
    id = PlaceHolder(
        0,
        """
        The represented application command's identifier number.
        
        Returns
        -------
        application_command_id : `int`
        """,
    )
    
    
    name = PlaceHolder(
        '',
        """
        The represented application command's name.
        
        Returns
        -------
        application_command_name : `str`
        """,
    )
    
    
    options = PlaceHolder(
        None,
        """
        Application command option representations. Like sub-command or parameter.
            
        Returns
        -------
        options : `None`, `tuple` of ``InteractionOption``
        """,
    )
    
    
    resolved = PlaceHolder(
        None,
        """
        Contains the received entities.
        
        Returns
        -------
        resolved : `None`, ``Resolved``
        """,
    )
    
    
    target_id = PlaceHolder(
        0,
        """
        The interaction's target's identifier. Applicable for context commands.
        
        Returns
        -------
        target_id : `int`
        """,
    )
    
    
    values = PlaceHolder(
        None,
        """
        Values selected by the user. Applicable for component interactions.
        
        Returns
        -------
        values : `None`, `tuple` of `str`
        """
    )
    
    # Extra utility | Application command
    
    @property
    def target(self):
        """
        Returns the application command's target. Applicable if the interaction was invoked by a context command.
        
        Returns
        -------
        entity : `None` ``Attachment``, ``Channel``, ``ClientUserBase``, ``Role``, ``Message``
        """
        target_id = self.target_id
        if target_id:
            return self.resolve_entity(target_id)
    
    # Extra utility
    
    # Application command autocomplete
    
    def iter_options(self):
        """
        Iterates over the options of the interaction application command (autocomplete) interaction.
        
        This method is an iterable generator.
        
        Yields
        ------
        option : ``InteractionOption``
        """
        options = self.options
        if (options is not None):
            yield from options
    
    
    @property
    def focused_option(self):
        """
        Returns the focused option of the application command autocomplete interaction.
        
        Returns
        -------
        option : `None`, ``InteractionOption``
        """
        for option in self.iter_options():
            focused_option = option.focused_option
            if (focused_option is not None):
                return focused_option
    
    
    def get_non_focused_values(self):
        """
        Gets the non focused values of the interaction.
        
        Returns
        -------
        non_focused_options : `dict` of (`str`, (`None`, `str`)) items
        """
        return dict(self._iter_non_focused_values())
    
    
    def _iter_non_focused_values(self):
        """
        Iterates over the non focused values of the interaction.
        
        This method is an iterable generator.
        
        Yields
        ------
        name : `str`
            The option's name.
        
        value : `None`, `str`
            The option's value.
        """
        for option in self.iter_options():
            yield from option._iter_non_focused_values()
    
    
    def get_value_of(self, *option_names):
        """
        Gets the value for the option by the given name.
        
        Parameters
        ----------
        *option_names : `str`
            The option(s)'s name.
        
        Returns
        -------
        value : `None`, `str`
            The value, the user has been typed.
        """
        if not option_names:
            return
            
        option_name, *option_names = option_names
        
        for option in self.iter_options():
            if option.name == option_name:
                return option.get_value_of(*option_names)
    
    
    @property
    def value(self):
        """
        Returns the focused option's value of the application command autocomplete interaction.
        
        Returns
        -------
        value : `None`, `str`
        """
        focused_option = self.focused_option
        if (focused_option is not None):
            return focused_option.value
    
    # Message component
    
    def iter_values(self):
        """
        Iterates over the values selected by the user.
        
        This method is an iterable generator.
        
        Yields
        ------
        value : `str`
        """
        values = self.values
        if (values is not None):
            yield from values
    
    
    def iter_entities(self):
        """
        Iterates over the entities that were selected by the user of a select component interaction.
        
        This method is an iterable generator.
        
        Yields
        ------
        entity : ``Channel``, ``ClientUserbase``, ``Role``
        """
        resolved = self.resolved
        if resolved is None:
            return
        
        values = self.values
        if values is None:
            return
        
        try:
            resolver = ENTITY_RESOLVERS[self.component_type]
        except KeyError:
            return
        
        for value in values:
            try:
                entity_id = int(value)
            except ValueError:
                continue
            
            entity = resolver(resolved, entity_id)
            if (entity is not None):
                yield entity
    
    
    @property
    def entities(self):
        """
        Returns the entities that were selected by the user of a select component interaction.
        
        Returns
        -------
        entities : `list` of (``Channel``, ``ClientUserbase``, ``Role``)
        """
        return [*self.iter_entities()]
    
    # Form submit
    
    def iter_components(self):
        """
        Iterates over the sub-components of a form-submit interaction.
        
        This method is an iterable generator.
        
        Yields
        ------
        component : ``InteractionComponent``
        """
        components = self.components
        if (components is not None):
            yield from components
    
    
    def iter_custom_ids_and_values(self):
        """
        Iterates over all the `custom_id`-s and values of the form submit interaction.
        
        This method is an iterable generator.
        
        Yields
        ------
        custom_id : `str`
            The `custom_id` of a represented component.
        value : `str`
            The `value` passed by the user.
        """
        for component in self.iter_components():
            yield from component.iter_custom_ids_and_values()
    
    
    def get_custom_id_value_relation(self):
        """
        Returns a dictionary with `custom_id` to `value` relation.
        
        Returns
        -------
        custom_id_value_relation : `dict` of (`str`, `str`) items
        """
        custom_id_value_relation = {}
        
        for custom_id, value in self.iter_custom_ids_and_values():
            if (value is not None):
                custom_id_value_relation[custom_id] = value
        
        return custom_id_value_relation
    
    
    def get_value_for(self, custom_id_to_match):
        """
        Returns the value for the given `custom_id`.
        
        Parameters
        ----------
        custom_id_to_match : `str`
            A respective components `custom_id` to match.
        
        Returns
        -------
        value : `None`, `str`
            The value if any.
        """
        for custom_id, value in self.iter_custom_ids_and_values():
            if (custom_id == custom_id_to_match):
                return value
    
    
    def get_match_and_value(self, matcher):
        """
        Gets a `custom_id`'s value matching the given `matcher`.
        
        Parameters
        ----------
        matcher : `callable`
            Matcher to call on a `custom_id`
            
            Should accept the following parameters:
            
            +-----------+-----------+
            | Name      | Type      |
            +===========+===========+
            | custom_id | `str`     |
            +-----------+-----------+
            
            Should return non-`None` on success.
        
        Returns
        -------
        match : `None`, `Any`
            The returned value by the ``matcher``
        value : `None`, `str`
            The matched `custom_id`'s value.
        """
        for custom_id, value in self.iter_custom_ids_and_values():
            match = matcher(custom_id)
            if (match is not None):
                return match, value
        
        return None, None
    
    
    def iter_matches_and_values(self, matcher):
        """
        Gets a `custom_id`'s value matching the given `matcher`.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        matcher : `callable`
            Matcher to call on a `custom_id`
            
            Should accept the following parameters:
            
            +-----------+-----------+
            | Name      | Type      |
            +===========+===========+
            | custom_id | `str`     |
            +-----------+-----------+
            
            Should return non-`None` on success.
        
        Yields
        -------
        match : `None`, `Any`
            The returned value by the ``matcher``
        value : `None`, `str`
            The matched `custom_id`'s value.
        """
        for custom_id, value in self.iter_custom_ids_and_values():
            match = matcher(custom_id)
            if (match is not None):
                yield match, value
    
    # resolved
    
    @copy_docs(Resolved.resolve_attachment)
    def resolve_attachment(self, attachment_id):
        resolved = self.resolved
        if (resolved is not None):
            return resolved.resolve_attachment(attachment_id)
    
    
    @copy_docs(Resolved.resolve_channel)
    def resolve_channel(self, channel_id):
        resolved = self.resolved
        if (resolved is not None):
            return resolved.resolve_channel(channel_id)
    
    
    @copy_docs(Resolved.resolve_role)
    def resolve_role(self, role_id):
        resolved = self.resolved
        if (resolved is not None):
            return resolved.resolve_role(role_id)
    
    
    @copy_docs(Resolved.resolve_message)
    def resolve_message(self, message_id):
        resolved = self.resolved
        if (resolved is not None):
            return resolved.resolve_message(message_id)
    
    
    @copy_docs(Resolved.resolve_user)
    def resolve_user(self, user_id):
        resolved = self.resolved
        if (resolved is not None):
            return resolved.resolve_user(user_id)
    
    
    @copy_docs(Resolved.resolve_mentionable)
    def resolve_mentionable(self, mentionable_id):
        resolved = self.resolved
        if (resolved is not None):
            return resolved.resolve_mentionable(mentionable_id)
    
    
    @copy_docs(Resolved.resolve_entity)
    def resolve_entity(self, entity_id):
        resolved = self.resolved
        if (resolved is not None):
            return resolved.resolve_entity(entity_id)
