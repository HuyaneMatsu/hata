__all__ = ('MessageInteraction',)

from warnings import warn

from scarletio import export, include

from ...bases import DiscordEntity
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...user import User, ZEROUSER, create_partial_user_from_id

from .fields import (
    parse_authorizer_user_ids, parse_id, parse_interacted_message_id, parse_name_and_sub_command_name_stack,
    parse_response_message_id, parse_target_message_id, parse_target_user, parse_triggering_interaction, parse_type,
    parse_user, put_authorizer_user_ids_into, put_id_into, put_interacted_message_id_into,
    put_name_and_sub_command_name_stack_into, put_response_message_id_into, put_target_message_id_into,
    put_target_user_into, put_triggering_interaction_into, put_type_into, put_user_into, validate_authorizer_user_ids,
    validate_id, validate_interacted_message_id, validate_name, validate_response_message_id,
    validate_sub_command_name_stack, validate_target_message_id, validate_target_user, validate_triggering_interaction,
    validate_type, validate_user
)


InteractionType = include('InteractionType')


PRECREATE_FIELDS = {
    'authorizer_users': ('authorizer_user_ids', validate_authorizer_user_ids),
    'authorizer_user_ids': ('authorizer_user_ids', validate_authorizer_user_ids),
    'interacted_message': ('interacted_message_id', validate_interacted_message_id),
    'interacted_message_id': ('interacted_message_id', validate_interacted_message_id),
    'interaction_type': ('type', validate_type),
    'name': ('name', validate_name),
    'response_message': ('response_message_id', validate_response_message_id),
    'response_message_id': ('response_message_id', validate_response_message_id),
    'sub_command_name_stack': ('sub_command_name_stack', validate_sub_command_name_stack),
    'target_message': ('target_message_id', validate_target_message_id),
    'target_message_id': ('target_message_id', validate_target_message_id),
    'target_user': ('target_user', validate_target_user),
    'triggering_interaction': ('triggering_interaction', validate_triggering_interaction),
    'user': ('user', validate_user),
}


@export   
class MessageInteraction(DiscordEntity):
    """
    Sent with a ``Message`` when the it is a response to an ``InteractionEvent``.
    
    Attributes
    ----------
    authorizer_user_ids : `None | dict<ApplicationIntegrationType, int>`
        The users' identifier who authorized the integration.
    
    id : `int`
        The interaction's identifier.
    
    interacted_message_id : `int`
        The interacted message's identifier. Present if the message is created from a component interaction.
    
    name : `str`
        The invoked interaction's name.
    
    response_message_id : `int`
        The response message's identifier. Present if the message is a followup one.
    
    sub_command_name_stack : `None | tuple<str>`
        The sub-command-group and sub-command names.
    
    target_message_id : `int`
        The targeted message's identifier in case of a message context interaction.
    
    target_user : `None | ClientUserBase`
        The targeted message's identifier in case of a user context interaction.
    
    triggering_interaction : `None | MessageInteraction`
        Represents the source form interaction. Present if the message is created from a form interaction.
    
    type : ``InteractionType``
        The interaction's type.
    
    user : ``ClientUserBase``
        The user who invoked the interaction.
    """
    __slots__ = (
        'authorizer_user_ids', 'interacted_message_id', 'name', 'response_message_id', 'sub_command_name_stack',
        'target_message_id', 'target_user', 'triggering_interaction', 'type', 'user'
    )
    
    def __new__(
        cls,
        *,
        authorizer_user_ids = ...,
        interacted_message_id = ...,
        interaction_type = ...,
        name = ...,
        response_message_id = ...,
        sub_command_name_stack = ...,
        target_message_id = ...,
        target_user = ...,
        triggering_interaction = ...,
        user = ...,
        user_id = ...,
    ):
        """
        Creates a new message interaction with the given fields.
        
        Parameters
        ----------
        authorizer_user_ids : `None | dict<ApplicationIntegrationType | int, int | ClientUserBase>` \
                , Optional (Keyword only)
            The users' identifier who authorized the integration.
        
        interacted_message_id : `int`, `None`, ``Message``, Optional (Keyword only)
            The interacted message's identifier. Present if the message is created from a component interaction.
        
        interaction_type : ``InteractionType``, `int`, Optional (Keyword only)
            The interaction's type.
        
        name : `str`, Optional (Keyword only)
            The invoked interaction's name.
        
        response_message_id : `int`, `None`, ``Message``, Optional (Keyword only)
            The response message's identifier. Present if the message is a followup one.
        
        sub_command_name_stack : `None`, `iterable` of `str`, Optional (Keyword only)
            The sub-command-group and sub-command names.
        
        target_message_id : `int | Message`, Optional (Keyword only)
            The targeted message's identifier in case of a message context interaction.
        
        target_user : `None | ClientUserBase`, Optional (Keyword only)
            The targeted message's identifier in case of a user context interaction.
        
        triggering_interaction : `None | MessageInteraction`, Optional (Keyword only)
            Represents the source form interaction. Present if the message is created from a form interaction.
        
        user : `None`, ``ClientUserBase``, Optional (Keyword only)
            The user who invoked the interaction.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # Deprecations
        if user_id is not ...:
            warn(
                (
                    f'`{cls.__name__}.__new__`\' `user_id` parameter is deprecated and will be removed in 2025 January. '
                    f'Please use `user` instead.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            user = User.precreate(user_id)
        
        # authorizer_user_ids
        if authorizer_user_ids is ...:
            authorizer_user_ids = None
        else:
            authorizer_user_ids = validate_authorizer_user_ids(authorizer_user_ids)
        
        # interacted_message_id
        if interacted_message_id is ...:
            interacted_message_id = 0
        else:
            interacted_message_id = validate_interacted_message_id(interacted_message_id)
        
        # interaction_type
        if interaction_type is ...:
            interaction_type = InteractionType.none
        else:
            interaction_type = validate_type(interaction_type)
        
        # response_message_id
        if response_message_id is ...:
            response_message_id = 0
        else:
            response_message_id = validate_response_message_id(response_message_id)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # sub_command_name_stack
        if sub_command_name_stack is ...:
            sub_command_name_stack = None
        else:
            sub_command_name_stack = validate_sub_command_name_stack(sub_command_name_stack)
        
        # target_message_id
        if target_message_id is ...:
            target_message_id = 0
        else:
            target_message_id = validate_target_message_id(target_message_id)
        
        # target_user
        if target_user is ...:
            target_user = None
        else:
            target_user = validate_target_user(target_user)
        
        # triggering_interaction
        if triggering_interaction is ...:
            triggering_interaction = None
        else:
            triggering_interaction = validate_triggering_interaction(triggering_interaction)
        
        # user
        if user is ...:
            user = ZEROUSER
        else:
            user = validate_user(user)
        
        # Construct
        self = object.__new__(cls)
        self.authorizer_user_ids = authorizer_user_ids
        self.id = 0
        self.interacted_message_id = interacted_message_id
        self.name = name
        self.response_message_id = response_message_id
        self.sub_command_name_stack = sub_command_name_stack
        self.target_message_id = target_message_id
        self.target_user = target_user
        self.triggering_interaction = triggering_interaction
        self.type = interaction_type
        self.user = user
        return self
    
    
    @classmethod
    def precreate(cls, message_interaction_id, **keyword_parameters):
        """
        Creates a new message interaction with the given predefined fields.
        
        > Since message interactions are not globally cached, this method is only used for testing.
        
        Parameters
        ----------
        authorizer_user_ids : `None | dict<ApplicationIntegrationType | int, int | ClientUserBase>` \
                , Optional (Keyword only)
            The users' identifier who authorized the integration.
        
        authorizer_users : `None | dict<ApplicationIntegrationType | int, int | ClientUserBase>` \
                , Optional (Keyword only)
            Alternative for `authorizer_user_ids`.
        
        message_interaction_id : `int`
            The message interaction's id.
        
        **keyword_parameters : Keyword parameters
            The attributes to set.
        
        Other Parameters
        ----------------
        interacted_message : `int`, `None`, ``Message``, Optional (Keyword only)
            Alternative for `interacted_message_id`.
        
        interacted_message_id : `int`, `None`, ``Message``, Optional (Keyword only)
            The interacted message's identifier. Present if the message is created from a component interaction.
        
        interaction_type : ``InteractionType``, `int`, Optional (Keyword only)
            The interaction's type.
        
        name : `str`, Optional (Keyword only)
            The invoked interaction's name.
        
        response_message : `int`, `None`, ``Message``, Optional (Keyword only)
            Alternative for `response_message_id`.
        
        response_message_id : `int`, `None`, ``Message``, Optional (Keyword only)
            The response message's identifier. Present if the message is a followup one.
        
        target_message : `int | Message`, Optional (Keyword only)
            Alternative for `target_message_id`.
        
        target_message_id : `int | Message`, Optional (Keyword only)
            The targeted message's identifier in case of a message context interaction.
        
        target_user : `None | ClientUserBase`, Optional (Keyword only)
            The targeted message's identifier in case of a user context interaction.
        
        
        sub_command_name_stack : `None`, `iterable` of `str`, Optional (Keyword only)
            The sub-command-group and sub-command names.
        
        triggering_interaction : `None | MessageInteraction`, Optional (Keyword only)
            Represents the source form interaction. Present if the message is created from a form interaction.
        
        user : `None`, ``ClientUserBase``, Optional (Keyword only)
            The user who invoked the interaction.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra or unused parameters.
        ValueError
            - If a parameter's value is incorrect.
        """
        message_interaction_id = validate_id(message_interaction_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        self = cls._create_empty(message_interaction_id)
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    @classmethod
    def _create_empty(cls, message_interaction_id):
        """
        Creates a new message interaction with it's defaults attributes set.
        
        Parameters
        ----------
        message_interaction_id : `int`
            The message interaction's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.authorizer_user_ids = None
        self.id = message_interaction_id
        self.interacted_message_id = 0
        self.name = ''
        self.response_message_id = 0
        self.sub_command_name_stack = None
        self.target_message_id = 0
        self.target_user = None
        self.triggering_interaction = None
        self.type = InteractionType.none
        self.user = ZEROUSER
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new message interaction from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Message interaction data.
        
        Returns
        -------
        data : `instance<cls>`
        """
        self = object.__new__(cls)
        
        self.authorizer_user_ids = parse_authorizer_user_ids(data)
        self.id = parse_id(data)
        self.interacted_message_id = parse_interacted_message_id(data)
        self.name, self.sub_command_name_stack = parse_name_and_sub_command_name_stack(data)
        self.response_message_id = parse_response_message_id(data)
        self.target_message_id = parse_target_message_id(data)
        self.target_user = parse_target_user(data)
        self.triggering_interaction = parse_triggering_interaction(data)
        self.type = parse_type(data)
        self.user = parse_user(data)
        
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Tries to convert the message interaction back to json serializable dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`)
        """
        data = {}
        put_authorizer_user_ids_into(self.authorizer_user_ids, data, defaults)
        put_interacted_message_id_into(self.interacted_message_id, data, defaults)
        put_name_and_sub_command_name_stack_into((self.name, self.sub_command_name_stack), data, defaults)
        put_response_message_id_into(self.response_message_id, data, defaults)
        put_target_message_id_into(self.target_message_id, data, defaults)
        put_target_user_into(self.target_user, data, defaults)
        put_triggering_interaction_into(
            self.triggering_interaction, data, defaults, include_internals = include_internals
        )
        put_type_into(self.type, data, defaults)
        
        if include_internals:
            put_user_into(self.user, data, defaults)
            put_id_into(self.id, data, defaults)
        
        return data
    
    
    @property
    def partial(self):
        """
        Returns whether the message interaction is partial.
        
        Returns
        -------
        partial : `bool`
        """
        return (self.id == 0)
    
    
    def __repr__(self):
        """Returns the message interaction's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # id
        interaction_id = self.id
        if interaction_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(interaction_id))
            repr_parts.append(',')
        else:
            repr_parts.append(' (partial)')
            
        # type
        interaction_type = self.type
        repr_parts.append(' type = ')
        repr_parts.append(interaction_type.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(interaction_type.value))
        
        # name
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        # sub_command_name_stack
        sub_command_name_stack = self.sub_command_name_stack
        if (sub_command_name_stack is not None):
            repr_parts.append(', sub_command_name_stack = ')
            repr_parts.append(repr(sub_command_name_stack))
        
        # user
        repr_parts.append(', user = ')
        repr_parts.append(repr(self.user))
        
        # authorizer_user_ids
        authorizer_user_ids = self.authorizer_user_ids
        if (authorizer_user_ids is not None):
            repr_parts.append(', authorizer_user_ids = ')
            repr_parts.append(repr(authorizer_user_ids))
        
        # interacted_message_id
        interacted_message_id = self.interacted_message_id
        if (interacted_message_id is not None):
            repr_parts.append(', interacted_message_id = ')
            repr_parts.append(repr(interacted_message_id))
        
        # response_message_id
        response_message_id = self.response_message_id
        if response_message_id:
            repr_parts.append(', response_message_id = ')
            repr_parts.append(repr(response_message_id))
        
        # target_message_id
        target_message_id = self.target_message_id
        if target_message_id:
            repr_parts.append(', target_message_id = ')
            repr_parts.append(repr(target_message_id))
        
        # target_user
        target_user = self.target_user
        if target_user:
            repr_parts.append(', target_user = ')
            repr_parts.append(repr(target_user))
        
        # triggering_interaction
        triggering_interaction = self.triggering_interaction
        if (triggering_interaction is not None):
            repr_parts.append(', triggering_interaction = ')
            repr_parts.append(repr(triggering_interaction))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two message interactions are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two message interactions not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `instance<type<<self>>`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        # id
        self_id = self.id
        other_id = other.id
        if self_id and other_id and self_id != other_id:
            return False
        
        # authorizer_user_ids
        if self.authorizer_user_ids != other.authorizer_user_ids:
            return False
        
        # interacted_message_id
        if self.interacted_message_id != other.interacted_message_id:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # response_message_id
        if self.response_message_id != other.response_message_id:
            return False
        
        # sub_command_name_stack
        if self.sub_command_name_stack != other.sub_command_name_stack:
            return False
        
        # target_message_id
        if self.target_message_id != other.target_message_id:
            return False
        
        # target_user
        if self.target_user is not other.target_user:
            return False
        
        # triggering_interaction
        if self.triggering_interaction != other.triggering_interaction:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        # user
        if self.user is not other.user:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the message integration's hash value."""
        hash_value = 0
        
        # authorizer_user_ids
        authorizer_user_ids = self.authorizer_user_ids
        if (authorizer_user_ids is not None):
            hash_value ^= len(authorizer_user_ids) << 8
            for integration_type, user_id in authorizer_user_ids.items():
                hash_value ^= (integration_type.value << 22) & user_id
        
        # id
        hash_value ^= self.id
        
        # interacted_message_id
        hash_value ^= self.interacted_message_id
        
        # name
        hash_value ^= hash(self.name)
        
        # response_message_id
        hash_value ^= self.response_message_id
        
        # sub_command_name_stack
        sub_command_name_stack = self.sub_command_name_stack
        if (sub_command_name_stack is not None):
            hash_value ^= len(sub_command_name_stack)
            for sub_command_name in sub_command_name_stack:
                hash_value ^= hash(sub_command_name)
        
        # target_message_id
        hash_value ^= self.target_message_id
        
        # target_user
        target_user = self.target_user
        if (target_user is not None):
            hash_value ^= target_user.id
        
        # triggering_interaction
        triggering_interaction = self.triggering_interaction
        if (triggering_interaction is not None):
            hash_value ^= hash(triggering_interaction)
        
        # type
        hash_value ^= self.type.value << 4
        
        # user
        hash_value ^= hash(self.user)
        
        return hash_value
    
    
    
    def copy(self):
        """
        Copies the message application returning a new partial one.
        
        Returns
        -------
        new : `instance<cls>`
        """
        new = object.__new__(type(self))
        
        authorizer_user_ids = self.authorizer_user_ids
        if (authorizer_user_ids is not None):
            authorizer_user_ids = authorizer_user_ids.copy()
        new.authorizer_user_ids = authorizer_user_ids
        
        new.id = 0
        new.interacted_message_id = self.interacted_message_id
        new.name = self.name
        new.response_message_id = self.response_message_id
        
        sub_command_name_stack = self.sub_command_name_stack
        if (sub_command_name_stack is not None):
            sub_command_name_stack = (*sub_command_name_stack,)
        new.sub_command_name_stack = sub_command_name_stack
        
        new.target_message_id = self.target_message_id
        new.target_user = self.target_user
        
        triggering_interaction = self.triggering_interaction
        if (triggering_interaction is not None):
            triggering_interaction = triggering_interaction.copy()
        new.triggering_interaction = triggering_interaction
        
        new.type = self.type
        new.user = self.user
        
        return new
    
    
    def copy_with(
        self,
        *,
        authorizer_user_ids = ...,
        interacted_message_id = ...,
        interaction_type = ...,
        name = ...,
        response_message_id = ...,
        sub_command_name_stack = ...,
        target_message_id = ...,
        target_user = ...,
        triggering_interaction = ...,
        user = ...,
        user_id = ...,
    ):
        """
        Copies the message interaction with the given fields returning a new partial one.
        
        Parameters
        ----------
        authorizer_user_ids : `None | dict<ApplicationIntegrationType | int, int | ClientUserBase>` \
                , Optional (Keyword only)
            The users' identifier who authorized the integration.
        
        interacted_message_id : `int`, `None`, ``Message``, Optional (Keyword only)
            The interacted message's identifier. Present if the message is created from a component interaction.
        
        interaction_type : ``InteractionType``, `int`, Optional (Keyword only)
            The interaction's type.
        
        name : `str`, Optional (Keyword only)
            The invoked interaction's name.
        
        response_message_id : `int`, `None`, ``Message``, Optional (Keyword only)
            The response message's identifier. Present if the message is a followup one.
        
        sub_command_name_stack : `None`, `iterable` of `str`, Optional (Keyword only)
            The sub-command-group and sub-command names.
        
        target_message_id : `int | Message`, Optional (Keyword only)
            The targeted message's identifier in case of a message context interaction.
        
        target_user : `None | ClientUserBase`, Optional (Keyword only)
            The targeted message's identifier in case of a user context interaction.
        
        triggering_interaction : `None | MessageInteraction`, Optional (Keyword only)
            Represents the source form interaction. Present if the message is created from a form interaction.
        
        user : `None`, ``ClientUserBase``, Optional (Keyword only)
            The user who invoked the interaction.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # Deprecations
        if user_id is not ...:
            warn(
                (
                    f'`{type(self).__name__}.copy_with`\' `user_id` parameter is deprecated '
                    f'and will be removed in 2024 December. Please use `user` instead.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            user = User.precreate(user_id)
        
        # authorizer_user_ids
        if authorizer_user_ids is ...:
            authorizer_user_ids = self.authorizer_user_ids
            if (authorizer_user_ids is not None):
                authorizer_user_ids = authorizer_user_ids.copy()
        else:
            authorizer_user_ids = validate_authorizer_user_ids(authorizer_user_ids)
        
        # interacted_message_id
        if interacted_message_id is ...:
            interacted_message_id = self.interacted_message_id
        else:
            interacted_message_id = validate_interacted_message_id(interacted_message_id)
        
        # interaction_type
        if interaction_type is ...:
            interaction_type = self.type
        else:
            interaction_type = validate_type(interaction_type)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # response_message_id
        if response_message_id is ...:
            response_message_id = self.response_message_id
        else:
            response_message_id = validate_response_message_id(response_message_id)
        
        # sub_command_name_stack
        if sub_command_name_stack is ...:
            sub_command_name_stack = self.sub_command_name_stack
            if (sub_command_name_stack is not None):
                sub_command_name_stack = (*sub_command_name_stack,)
        else:
            sub_command_name_stack = validate_sub_command_name_stack(sub_command_name_stack)
        
        # target_message_id
        if target_message_id is ...:
            target_message_id = self.target_message_id
        else:
            target_message_id = validate_target_message_id(target_message_id)
        
        # target_user
        if target_user is ...:
            target_user = self.target_user
        else:
            target_user = validate_target_user(target_user)
        
        # triggering_interaction
        if triggering_interaction is ...:
            triggering_interaction = self.triggering_interaction
            if (triggering_interaction is not None):
                triggering_interaction = triggering_interaction.copy()
        else:
            triggering_interaction = validate_triggering_interaction(triggering_interaction)
        
        # user
        if user is ...:
            user = self.user
        else:
            user = validate_user(user)
    
        # Construct
        new = object.__new__(type(self))
        new.authorizer_user_ids = authorizer_user_ids
        new.id = 0
        new.interacted_message_id = interacted_message_id
        new.name = name
        new.response_message_id = response_message_id
        new.sub_command_name_stack = sub_command_name_stack
        new.target_message_id = target_message_id
        new.target_user = target_user
        new.triggering_interaction = triggering_interaction
        new.type = interaction_type
        new.user = user
        return new
    
    
    @property
    def joined_name(self):
        """
        Returns the joined name of the message interaction.
        
        Returns
        -------
        joined_name : `str`
        """
        name = self.name
        sub_command_name_stack = self.sub_command_name_stack
        if (sub_command_name_stack is None):
            return name
        
        return ' '.join([name, *sub_command_name_stack])
    
    
    @property
    def user_id(self):
        """
        Returns the user's identifier who invoked the interaction.
        
        Returns
        -------
        user_id : `int`
        """
        return self.user.id
    
    
    def get_authorizer_user_id(self, integration_type):
        """
        Gets the authorizer user's identifier for the given integration type.
        
        Parameters
        ----------
        integration_type : `ApplicationIntegrationType | int`
            Integration type to query for.
        
        Returns
        -------
        user_id : `int`
        """
        authorizer_user_ids = self.authorizer_user_ids
        if (authorizer_user_ids is not None):
            try:
                return authorizer_user_ids[integration_type]
            except KeyError:
                pass
        
        return 0
    
    
    def get_authorizer_user(self, integration_type):
        """
        Gets the authorizer user for the given integration type.
        
        Parameters
        ----------
        integration_type : `ApplicationIntegrationType | int`
            Integration type to query for.
        
        Returns
        -------
        user : `None | ClientUserBase`
        """
        user_id = self.get_authorizer_user_id(integration_type)
        if user_id:
            return create_partial_user_from_id(user_id)

    
    @property
    def target_user_id(self):
        """
        Returns the targeted user's identifier.
        
        Returns
        -------
        target_user_id : `int`
        """
        target_user = self.target_user
        if target_user is None:
            return 0
        
        return target_user.id
