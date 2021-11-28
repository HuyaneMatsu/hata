__all__ = ('ApplicationCommandAutocompleteInteraction', 'ApplicationCommandAutocompleteInteractionOption',
    'ApplicationCommandInteraction', 'ApplicationCommandInteractionOption', 'ComponentInteraction',
    'FormSubmitInteraction', 'FormSubmitInteractionOption', 'InteractionEvent', 'InteractionResponseContext',
    'InteractionType')


import reprlib, warnings

from ...backend.export import export
from ...backend.futures import Future, shield, future_or_timeout

from ..bases import EventBase, DiscordEntity
from ..core import KOKORO, INTERACTION_EVENT_RESPONSE_WAITERS, INTERACTION_EVENT_MESSAGE_WAITERS, CHANNELS, GUILDS, \
    APPLICATION_ID_TO_CLIENT
from ..channel import create_partial_channel_from_data
from ..message import Message
from ..permission import Permission
from ..permission.permission import PERMISSION_PRIVATE
from ..guild import create_partial_guild_from_id
from ..user import User, ClientUserBase
from ..role import Role

from .components import ComponentBase
from .preinstanced import ApplicationCommandOptionType, InteractionType, ComponentType


RESPONSE_FLAG_DEFERRING = 1<<0
RESPONSE_FLAG_DEFERRED = 1<<1
RESPONSE_FLAG_RESPONDING = 1<<2
RESPONSE_FLAG_RESPONDED = 1<<3
RESPONSE_FLAG_EPHEMERAL = 1<<4

RESPONSE_FLAG_NONE = 0
RESPONSE_FLAG_ACKNOWLEDGING = RESPONSE_FLAG_DEFERRING|RESPONSE_FLAG_RESPONDING
RESPONSE_FLAG_ACKNOWLEDGED = RESPONSE_FLAG_DEFERRED|RESPONSE_FLAG_RESPONDED
RESPONSE_FLAG_DEFERRING_OR_DEFERRED = RESPONSE_FLAG_DEFERRING|RESPONSE_FLAG_DEFERRED
RESPONSE_FLAG_RESPONDING_OR_RESPONDED = RESPONSE_FLAG_RESPONDING|RESPONSE_FLAG_RESPONDED
RESPONSE_FLAG_ACKNOWLEDGING_OR_ACKNOWLEDGED = RESPONSE_FLAG_ACKNOWLEDGING|RESPONSE_FLAG_ACKNOWLEDGED

INTERACTION_TYPE_APPLICATION_COMMAND = InteractionType.application_command


class ApplicationCommandInteraction(DiscordEntity):
    """
    Represents an ``ApplicationCommand`` invoked by a user.
    
    Attributes
    ----------
    id : `int`
        The represented application command's identifier number.
    name : `str`
        The name of the command. It's length can be in range [1:32].
    options : `None` or `tuple` of ``ApplicationCommandInteractionOption``
        The parameters and values from the user if any. Defaults to `None` if non is received.
    resolved_channels : `None` or `dict` of (`int`, ``ChannelBase``) items
        Resolved received channels stored by their identifier as keys if any.
    resolved_roles : `None` or `dict` of (`int`, ``Role``) items
        Resolved received roles stored by their identifier as keys if any.
    resolved_messages : `None` or `dict` of (`int`, ``Message``) items
        Resolved received messages stored by their identifier as keys if any.
    resolved_users : `None` or `dict` of (`int`, ``ClientUserBase``) items
        Resolved received users stored by their identifier as keys if any.
    target_id : `int`
        The interaction's target's identifier.
    """
    __slots__ = ('name', 'options', 'resolved_channels', 'resolved_roles', 'resolved_messages', 'resolved_users',
        'target_id',)
    
    def __new__(cls, data, interaction_event):
        """
        Creates a new ``ApplicationCommandInteraction`` from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received application command interaction data.
        interaction_event : ``InteractionEvent``
            The parent interaction event.
        """
        # id
        id_ = int(data['id'])
        
        # name
        name = data['name']
        
        # options
        option_datas = data.get('options', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = tuple(ApplicationCommandInteractionOption(option_data) for option_data in option_datas)
        
        # resolved_channels & resolved_roles & resolved_messages & resolved_users
        try:
            resolved_data = data['resolved']
        except KeyError:
            resolved_channels = None
            resolved_roles = None
            resolved_messages = None
            resolved_users = None
        else:
            # resolved_channels
            try:
                resolved_channel_datas = resolved_data['channels']
            except KeyError:
                resolved_channels = None
            else:
                if resolved_channel_datas:
                    resolved_channels = {}
                    
                    for channel_data in resolved_channel_datas.values():
                        channel = create_partial_channel_from_data(channel_data, interaction_event.id)
                        if (channel is not None):
                            resolved_channels[channel.id] = channel
                    
                    if not resolved_channels:
                        resolved_channels = None
                else:
                    resolved_channels = None
            
            # resolved_roles
            try:
                resolved_role_datas = resolved_data['roles']
            except KeyError:
                resolved_roles = None
            else:
                if resolved_role_datas:
                    resolved_roles = {}
                    for role_data in resolved_role_datas.values():
                        role = Role(role_data, interaction_event.guild)
                        resolved_roles[role.id] = role
                else:
                    resolved_roles = None
            
            # resolved_messages
            try:
                resolved_message_datas = resolved_data['messages']
            except KeyError:
                resolved_messages = None
            else:
                if resolved_message_datas:
                    resolved_messages = {}
                    
                    for message_data in resolved_message_datas.values():
                        message = Message(message_data)
                        resolved_messages[message.id] = message
                else:
                    resolved_messages = None
            
            # resolved_users
            try:
                resolved_user_datas = resolved_data['users']
            except KeyError:
                resolved_users = None
            else:
                if resolved_user_datas:
                    try:
                        resolved_guild_profile_datas = resolved_data['members']
                    except KeyError:
                        resolved_guild_profile_datas = None
                    
                    resolved_users = {}
                    
                    for user_id, user_data in resolved_user_datas.items():
                        if resolved_guild_profile_datas is None:
                            guild_profile_data = None
                        else:
                            guild_profile_data = resolved_guild_profile_datas.get(user_id, None)
                        
                        if (guild_profile_data is not None):
                            user_data['member'] = guild_profile_data
                        
                        user = User(user_data, interaction_event.guild)
                        resolved_users[user.id] = user
                        
                        if (guild_profile_data is not None):
                            interaction_event._add_cached_user(user)
                
                else:
                    resolved_users = None
        
        # target_id
        target_id = data.get('target_id', None)
        if target_id is None:
            target_id = 0
        else:
            target_id = int(target_id)
        
        self = object.__new__(cls)
        self.id = id_
        self.name = name
        self.options = options
        self.resolved_users = resolved_users
        self.resolved_channels = resolved_channels
        self.resolved_roles = resolved_roles
        self.resolved_messages = resolved_messages
        self.target_id = target_id
        
        interaction_event._add_response_waiter()
        
        return self
    
    
    def __repr__(self):
        """Returns the application command interaction's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' id=', repr(self.id),
            ', name=', repr(self.name),
        ]
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        
        target = self.target
        if (target is not None):
            repr_parts.append(', target=')
            repr_parts.append(repr(target))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two application command interactions are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # id
        if self.id != other.id:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        # resolved_channels
        if self.resolved_channels != other.resolved_channels:
            return False
        
        # resolved_roles
        if self.resolved_roles != other.resolved_roles:
            return False
        
        # resolved_messages
        if self.resolved_messages != other.resolved_messages:
            return False
        
        # resolved_users
        if self.resolved_users != other.resolved_users:
            return False
        
        # target_id
        if self.target_id != other.target_id:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the application command interaction."""
        hash_value = 0
        
        # id
        hash_value ^= self.id
        
        # name
        hash_value ^= hash(self.name)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= len(options)
            
            for option in options:
                hash_value ^= hash(option)
        
        # resolved_channels
        resolved_channels = self.resolved_channels
        if (resolved_channels is not None):
            hash_value ^= (len(resolved_channels)<<8)
            
            for channel_id in resolved_channels.keys():
                hash_value ^= channel_id
        
        # resolved_roles
        resolved_roles = self.resolved_roles
        if (resolved_roles is not None):
            hash_value ^= (len(resolved_roles)<<12)
            
            for role_id in resolved_roles.keys():
                hash_value ^= role_id
        
        # resolved_messages
        resolved_messages = self.resolved_messages
        if (resolved_messages is not None):
            hash_value ^= (len(resolved_messages)<<16)
            
            for message_id in resolved_messages.keys():
                hash_value ^= message_id
        
        # resolved_users
        resolved_users = self.resolved_users
        if (resolved_users is not None):
            hash_value ^= (len(resolved_users)<<20)
            
            for user_id in resolved_users.keys():
                hash_value ^= user_id
        
        # target_id
        hash_value ^= self.target_id
        
        return hash_value
    
    
    def resolve_entity(self, entity_id):
        """
        Tries to resolve the entity by the given identifier.
        
        Parameters
        ----------
        entity_id : ``int``
            The entity's identifier.
        
        Returns
        -------
        resolved : `None` or ``DiscordEntity``
            The resolved discord entity if found.
        """
        # Is used at `InteractionEvent.target`, which wanna access user and message first, so we check that two first.
        resolved_messages = self.resolved_messages
        if (resolved_messages is not None):
            try:
                entity = resolved_messages[entity_id]
            except KeyError:
                pass
            else:
                return entity
        
        
        resolved_users = self.resolved_users
        if (resolved_users is not None):
            try:
                entity = resolved_users[entity_id]
            except KeyError:
                pass
            else:
                return entity
        
        
        resolved_roles = self.resolved_roles
        if (resolved_roles is not None):
            try:
                entity = resolved_roles[entity_id]
            except KeyError:
                pass
            else:
                return entity
        
        
        resolved_channels = self.resolved_channels
        if (resolved_channels is not None):
            try:
                entity = resolved_channels[entity_id]
            except KeyError:
                pass
            else:
                return entity
        
        
        return None

    
    @property
    def target(self):
        """
        Returns the interaction event's target.
        
        Only applicable for context application commands.
        
        Returns
        -------
        target : ``ClientUserBase``, ``Message``
        """
        target_id = self.target_id
        if target_id:
            return self.resolve_entity(target_id)


class ApplicationCommandInteractionOption:
    """
    Represents an option of a ``ApplicationCommandInteraction``.
    
    Attributes
    ----------
    name : `str`
        The option's name.
    
    options : `None` or `tuple` of ``ApplicationCommandInteractionOption``
        The parameters and values from the user. Present if a sub-command was used. Defaults to `None` if non is
        received.
        
        Mutually exclusive with the `value` field.
    
    type : ``ApplicationCommandOptionType``
        The option's type.
    
    value : `None`, `str`
        The given value by the user. Should be always converted to the expected type.
        
        Mutually exclusive with the `options` field,
    
    """
    __slots__ = ('name', 'options', 'type', 'value')
    
    def __new__(cls, data):
        """
        Creates a new ``ApplicationCommandInteractionOption`` instance from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received application command interaction option data.
        """
        # name
        name = data['name']
        
        # options
        option_datas = data.get('options', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = tuple(ApplicationCommandInteractionOption(option_data) for option_data in option_datas)
        
        # type
        type_ = ApplicationCommandOptionType.get(data.get('type', 0))
        
        # value
        value = data.get('value', None)
        if (value is not None):
            value = str(value)
        
        self = object.__new__(cls)
        
        self.name = name
        self.options = options
        self.type = type_
        self.value = value
        
        return self
    
    
    def __repr__(self):
        """Returns the application command interaction option's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ', name=', repr(self.name),
        ]
        
        type_ = self.type
        if type_ is not ApplicationCommandOptionType.none:
            repr_parts.append(', type=')
            repr_parts.append(type_.name)
            repr_parts.append(' (')
            repr_parts.append(repr(type_.value))
            repr_parts.append(')')
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        value = self.value
        if (value is not None):
            repr_parts.append(', value=')
            repr_parts.append(repr(value))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two application command interaction options are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # name
        if self.name != other.name:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        # value
        if self.value != other.value:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the application command interaction option's hash value."""
        hash_value = 0
        
        # name
        hash_value ^= hash(self.name)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= len(options)
            
            for option in options:
                hash_value ^= hash(option)
        
        # type
        hash_value ^= (self.type.value<<8)
        
        # value
        value = self.value
        if (value is not None):
            hash_value ^= hash(value)
        
        return hash_value


class ComponentInteraction:
    """
    A component interaction of an ``InteractionEvent``.
    
    Attributes
    ----------
    custom_id : `None` or `str`
        The component's custom identifier.
    options : `None` or `tuple` of `str`
        Option values selected of the respective interaction.
    type : ``ComponentType``
        The component's type.
    """
    __slots__ = ('type', 'custom_id', 'components', 'options')
    
    def __new__(cls, data, interaction_event):
        """
        Creates a new component interaction with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received application command interaction data.
        interaction_event : ``InteractionEvent``
            The parent interaction event.
        """
        # custom_id
        custom_id = data.get('custom_id', None)
        
        # type
        type_ = ComponentType.get(data['component_type'])
        
        # options
        option_datas = data.get('values', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = tuple(option_datas)
        
        self = object.__new__(cls)
        self.custom_id = custom_id
        self.options = options
        self.type = type_
        return self
    
    
    def __repr__(self):
        """Returns the component interaction's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # type
        type_ = self.type
        repr_parts.append(' type=')
        repr_parts.append(type_.name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_.value))
        repr_parts.append(')')
        
        custom_id = self.custom_id
        if (custom_id is not None):
            repr_parts.append(', custom_id=')
            repr_parts.append(reprlib.repr(custom_id))
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            index = 0
            limit = len(options)
            while True:
                option = options[index]
                repr_parts.append(repr(option))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Compares the two component or component interaction."""
        other_type = type(other)
        # Compare with self type.
        if other_type is type(self):
            # type
            if self.type is not other.type:
                return False
            #custom_id
            if self.custom_id != other.custom_id:
                return False
            
            return True
        
        # Compare with components.
        if issubclass(other_type, ComponentBase):
            # Check `type` before `custom_id`
            
            # type
            if self.type is not other.type:
                return False
            
            # custom_id
            if self.custom_id != other.custom_id:
                return False
            
            return True
        
        
        return NotImplemented
    
    
    def __hash__(self):
        """Returns the component interaction's hash value."""
        hash_value = 0
        
        # type
        hash_value ^= self.type.value
        
        # custom_id
        hash_value ^= hash(self.custom_id)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^ len(options)<<8
            for option in options:
                hash_value ^ hash(option)
        
        return hash_value
    
    
    def component_type(cls):
        """
        ``.component_type`` is deprecated, please use ``.type`` instead. Will be removed in 2022
        February.
        """
        warnings.warn(
            f'`{cls.__name__}.component_type` is deprecated, and will be removed in 2022 February. '
            f'Please use `{cls.__name__}.type` instead.',
            FutureWarning)
        
        return cls.type


class ApplicationCommandAutocompleteInteractionOption:
    """
    Application auto complete option representing an auto completable parameters.
    
    Attributes
    ----------
    focused : `bool`
        Whether this field is focused by the user.
    name : `str`
        The name of the parameter.
    options : `None` or `tuple` of ``ApplicationCommandAutocompleteInteractionOption``
        Nested functions.
    type : ``ApplicationCommandOptionType``
        The represented option's type.
    value : `None` or `str`
        The value, the user has been typed.
    """
    __slots__ = ('focused', 'name', 'options', 'type', 'value')
    
    def __new__(cls, data):
        """
        Creates a new ``ApplicationCommandAutocompleteOption`` instance from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`)
            Application command autocomplete option data.
        """
        # focused
        focused = data.get('focused', False)
        
        # name
        name = data['name']
        
        # options
        option_datas = data.get('options', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = tuple(
                ApplicationCommandAutocompleteInteractionOption(option_data) for option_data in option_datas
            )
        
        # type
        type_ = ApplicationCommandOptionType.get(data['type'])
        
        # value
        value = data.get('value', None)
        if (value is not None) and (not value):
            value = None
        
        self = object.__new__(cls)
        self.focused = focused
        self.name = name
        self.options = options
        self.type = type_
        self.value = value
        return self
    
    
    def __repr__(self):
        """Returns the application command autocomplete option's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' name=', repr(self.name),
        ]
        
        if self.focused:
            repr_parts.append(' (focused)')
        
        value = self.value
        if (value is not None):
            repr_parts.append(', value=')
            repr_parts.append(reprlib.repr(value))
        
        type_ = self.type
        repr_parts.append(', type=')
        repr_parts.append(type_.name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_.value))
        repr_parts.append(')')
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the application command autocomplete option's representation."""
        hash_value = 0
        
        # focused
        hash_value ^= (self.focused<<16)
        
        # name
        hash_value ^= hash(self.name)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= (len(options)<<8)
            
            for option in options:
                hash_value ^= hash(option)
        
        # type
        hash_value ^= self.type.value
        
        # value
        value = self.value
        if (value is not None):
            hash_value ^= hash(value)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two application command autocomplete option's are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # focused
        if self.focused != other.focused:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        # value
        if self.value != other.value:
            return False
        
        return True
    
    
    @property
    def focused_option(self):
        """
        Returns the focused option of the application command autocomplete interaction option.
        
        Returns
        -------
        option : `None` or ``ApplicationCommandAutocompleteInteractionOption``
        """
        if self.focused:
            return self
        
        options = self.options
        if (options is not None):
            for option in options:
                focused_option =  option.focused_option
                if (focused_option is not None):
                    return focused_option
    
    
    def get_value_of(self, *option_names):
        """
        Gets the value for the option by the given name.
        
        Parameters
        ----------
        *option_names : `str`
            The option(s)'s name.
        
        Returns
        -------
        value : `None` or `str`
            The value, the user has been typed.
        """
        if option_names:
            option_name, *option_names = option_names
            
            options = self.options
            if options is None:
                value = None
            else:
                for option in options:
                    if option.name == option_name:
                        value = option.get_value_of(*option_names)
                        break
                else:
                    value = None
        else:
            value = self.value
        
        return value


class ApplicationCommandAutocompleteInteraction:
    """
    Represents an ``ApplicationCommand``'s auto completion interaction.
    
    Attributes
    ----------
    id : `int`
        The represented application command's identifier number.
    name : `str`
        The name of the command. It's length can be in range [1:32].
    options : `None` or `tuple` of ``ApplicationCommandAutocompleteOption``
        Parameter auto completion options.
    """
    __slots__ = ('id', 'name', 'options',)
    
    def __new__(cls, data, interaction_event):
        """
        Creates a new ``ApplicationCommandAutocompleteInteraction`` from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received application command interaction data.
        interaction_event : ``InteractionEvent``
            The parent interaction event.
        """
        # id
        id_ = int(data['id'])
        
        # name
        name = data['name']
        
        # options
        option_datas = data.get('options', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = tuple(
                ApplicationCommandAutocompleteInteractionOption(option_data) for option_data in option_datas
            )
        
        self = object.__new__(cls)
        
        self.id = id_
        self.name = name
        self.options = options
        
        return self
    
    
    def __repr__(self):
        """Returns the application command interaction auto completion's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' id=', repr(self.id),
            ', name=', repr(self.name),
        ]
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the application command autocomplete interaction hash value."""
        hash_value = 0
        
        # id
        hash_value ^= self.id
        
        # name
        hash_value ^= hash(self.name)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= (len(options)<<8)
            
            for option in options:
                hash_value ^= hash(option)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two application command autocomplete interaction are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # id
        if self.id != other.id:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        return True
        
    
    @property
    def focused_option(self):
        """
        Returns the focused option of the application command autocomplete interaction.
        
        Returns
        -------
        option : `None` or ``ApplicationCommandAutocompleteInteractionOption``
        """
        options = self.options
        if options is None:
            focused_option = None
        else:
            for option in options:
                focused_option = option.focused_option
                if (focused_option is not None):
                    break
            else:
                focused_option = None
        
        return focused_option
    
    
    def get_value_of(self, *option_names):
        """
        Gets the value for the option by the given name.
        
        Parameters
        ----------
        *option_names : `str`
            The option(s)'s name.
        
        Returns
        -------
        value : `None` or `str`
            The value, the user has been typed.
        """
        if option_names:
            option_name, *option_names = option_names
            
            options = self.options
            if options is None:
                value = None
            else:
                for option in options:
                    if option.name == option_name:
                        value = option.get_value_of(*option_names)
                        break
                else:
                    value = None
        else:
            value = None
        
        return value
    
    
    @property
    def value(self):
        """
        Returns the focused option's value of the application command autocomplete interaction.
        
        Returns
        -------
        value : `None` or `str`
        """
        focused_option = self.focused_option
        if (focused_option is None):
            value = None
        else:
            value = focused_option.value
        
        return value


class FormSubmitInteraction:
    """
    Represents a response to a ``InteractionForm``.
    
    Attributes
    ----------
    custom_id : `None` or `str`
        The forms's custom identifier.
    options : `None` or `tuple` of ``FormSubmitInteractionOption``
        Submitted component values.
    """
    __slots__ = ('custom_id', 'options', )
    
    def __new__(cls, data, interaction_event):
        """
        Creates a new component interaction with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received form submit interaction data.
        interaction_event : ``InteractionEvent``
            The parent interaction event.
        """
        # custom_id
        custom_id = data.get('custom_id', None)
        if (custom_id is not None) and (not custom_id):
            custom_id = None
        
        # options
        option_datas = data.get('components', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = tuple(FormSubmitInteractionOption(option_data) for option_data in option_datas)
        
        
        self = object.__new__(cls)
        
        self.custom_id = custom_id
        self.options = options
        
        return self


    def __repr__(self):
        """Returns the form submit interaction's representation."""
        repr_parts = ['<', self.__class__.__name__,]
        
        repr_parts.append('custom_id=')
        repr_parts.append(self.custom_id)
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the form submit interaction's hash value."""
        hash_value = 0
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= (len(options)<<8)
            
            for option in options:
                hash_value ^= hash(option)
            
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two submit interactions are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        return True
    
    
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
        options = self.options
        if (options is not None):
            for option in options:
                yield from option.iter_custom_ids_and_values()
    
    
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
        value : `None` or `str`
            The value if any.
        """
        for custom_id, value in self.iter_custom_ids_and_values():
            if (custom_id == custom_id):
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
        match : `None` or `Any`
            The returned value by the ``matcher``
        value : `None` or `str`
            The matched `custom_id`'s value.
        """
        for custom_id, value in self.iter_custom_ids_and_values():
            match = matcher(custom_id)
            if (match is not None):
                return match, value


class FormSubmitInteractionOption:
    """
    Attributes
    ----------
    custom_id : `None` or `str`
        The option's respective component's type.
        
    options : `None` or `tuple` of ``FormSubmitInteractionOption``
        Mutually exclusive with the `value` field.
    
    type : ``ComponentType``
        The option respective component's type.
        
    value : `None` or `str`
        Mutually exclusive with the `options` field.
    """
    __slots__ = ('custom_id', 'options', 'type', 'value')
    
    def __new__(cls, data):
        """
        Creates a new ``FormSubmitInteractionOption`` from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received form submit interaction option data.
        """
        # custom_id
        custom_id = data.get('custom_id', None)
        if (custom_id is not None) and (not custom_id):
            custom_id = None
        
        # options
        option_datas = data.get('components', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = tuple(FormSubmitInteractionOption(option_data) for option_data in option_datas)
        
        # type
        type_ = ComponentType.get(data.get('type', 0))
        
        # value
        value = data.get('value', None)
        if (value is not None) and (not value):
            value = None
        
        self = object.__new__(cls)
        
        self.custom_id = custom_id
        self.options = options
        self.type = type_
        self.value = value
        
        return self
        
    def __repr__(self):
        """Returns the application command interaction option's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # Descriptive fields : type
        
        # type
        type_ = self.type
        if type_ is not ComponentType.none:
            repr_parts.append(', type=')
            repr_parts.append(type_.name)
            repr_parts.append(' (')
            repr_parts.append(repr(type_.value))
            repr_parts.append(')')
        
        # System fields : custom_id
        
        # custom_id
        repr_parts.append(', custom_id=')
        repr_parts.append(reprlib.repr(self.custom_id))
        
        # Extra descriptive fields : options | value
        # options
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        # value
        value = self.value
        if (value is not None):
            repr_parts.append(', value=')
            repr_parts.append(repr(value))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


    def __hash__(self):
        """Returns the form submit interaction's option hash value."""
        hash_value = 0
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= (len(options)<<8)
            
            for option in options:
                hash_value ^= hash(option)
        
        # type
        hash_value ^= self.type.value
        
        # value
        value = self.value
        if (value is not None):
            hash_value ^= hash(value)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two submit interaction options are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        # value
        if self.value != other.value:
            return False
        
        return True
    
    
    def iter_custom_ids_and_values(self):
        """
        Iterates over all the `custom_id`-s and values of the form submit interaction option.
        
        This method is an iterable generator.
        
        Yields
        ------
        custom_id : `str`
            The `custom_id` of a represented component.
        value : `str`
            The `value` passed by the user.
        """
        custom_id = self.custom_id
        if (custom_id is not None):
            yield custom_id, self.value
        
        options = self.options
        if (options is not None):
            for option in options:
                yield from option.iter_custom_ids_and_values()


INTERACTION_TYPE_TABLE = {
    InteractionType.ping.value: None,
    InteractionType.application_command.value: ApplicationCommandInteraction,
    InteractionType.message_component.value: ComponentInteraction,
    InteractionType.application_command_autocomplete.value: ApplicationCommandAutocompleteInteraction,
    InteractionType.form_submit: FormSubmitInteraction,
}


@export
class InteractionEvent(DiscordEntity, EventBase, immortal=True):
    """
    Represents a processed `INTERACTION_CREATE` dispatch event.
    
    Attributes
    ----------
    id : `int`
        The interaction's id.
    _cached_users : `None` or `list` of ``ClientUserBase``
        A list of users, which are temporary cached.
    _response_flag : `bool`
        The response order state of ``InteractionEvent``
        
        +-------------------------------+-------+---------------------------------------------------+
        | Respective name               | Shift | Description                                       |
        +===============================+=======+===================================================+
        | RESPONSE_FLAG_DEFERRING       | 0     | The vent is being acknowledged.                   |
        +-------------------------------+-------+---------------------------------------------------+
        | RESPONSE_FLAG_DEFERRED        | 1     | The event was acknowledged and response will be   |
        |                               |       | sent later. Shows loading screen for the user.    |
        +-------------------------------+-------+---------------------------------------------------+
        | RESPONSE_FLAG_RESPONDING      | 2     | Responding to the interaction.                    |
        +-------------------------------+-------+---------------------------------------------------+
        | RESPONSE_FLAG_RESPONDED       | 3     | Response was sent on the interaction.             |
        +-------------------------------+-------+---------------------------------------------------+
        | RESPONSE_FLAG_EPHEMERAL       | 4     | Whether the main response is an ephemeral,        |
        |                               |       | showing for the invoking user only.               |
        +-------------------------------+-------+---------------------------------------------------+
        
        Can be used by extensions and is used by the the ``Client`` instances to ensure correct flow order.
    application_id : `int`
        The interaction's application's identifier.
    channel_id : `int`
        The channel's identifier from where the interaction was called.
    guild_id : `int`
        The guild's identifier from where the interaction was called from. Might be `0` if the interaction was called
        from a private channel.
    interaction : `None` or ``ApplicationCommandInteraction``, ``ComponentInteraction`` or \
            ``ApplicationCommandAutocompleteInteraction``
        
        The called interaction by it's route by the user.
    message : `None` or ``Message``
        The message from where the interaction was received. Applicable for message components.
    token : `str`
        Interaction's token used when responding on it.
    type : ``InteractionType``
        The interaction's type.
    user : ``ClientUserBase``
        The user who called the interaction.
    user_permissions : ``Permission``
        The user's permissions in the respective channel.
    
    Class Attributes
    ----------------
    _USER_GUILD_CACHE : `dict` of (`tuple` (``ClientUserBase``, ``Guild``), `int`)
        A cache which stores `user-guild` pairs as keys and their reference count as values to remember
        ``InteractionEvent``'s ``.user``-s' guild profiles of the respective ``.guild`` even if the ``Guild`` is
        uncached.
    
        Note, that private channel interaction, neither interactions of cached guilds are not added, what means if
        all the clients are kicked from a guild the guild profile can be lost in unexpected time.
    
    Notes
    -----
    The interaction token can be used for 15 minutes, tho if it is not used within the first 3 seconds, it is
    invalidated immediately.
    
    ˙˙InteractionEvent˙˙ instances are weakreferable.
    """
    __slots__ = ('_cached_users', '_response_flag', 'application_id', 'channel_id', 'guild_id', 'interaction',
        'message', 'token', 'type', 'user', 'user_permissions')
    
    _USER_GUILD_CACHE = {}
    
    def __new__(cls, data):
        """
        Creates a new ``InteractionEvent`` instance with the given parameters.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            `INTERACTION_CREATE` dispatch event data.
        """
        # id_
        id_ = int(data['id'])
        
        # application_id
        application_id = int(data['application_id'])
        
        # channel_id
        channel_id = int(data['channel_id'])
        
        # guild_id
        guild_id = data.get('guild_id', None)
        if guild_id is None:
            guild_id = 0
        else:
            guild_id = int(guild_id)
        
        if guild_id:
            guild = create_partial_guild_from_id(guild_id)
        else:
            guild = None
        
        # interaction
        # We set interaction at the end when the object is fully initialized
        
        # message
        try:
            message_data = data['message']
        except KeyError:
            message = None
        else:
            message = Message(message_data)
        
        # token
        token = data['token']
        
        # type
        type_value = data['type']
        type_ = InteractionType.get(type_value)
        
        # user
        try:
            user_data = data['member']
        except KeyError:
            user_data = data['user']
        
        user = User(user_data, guild)
        
        # user_permissions
        try:
            user_permissions = user_data['permissions']
        except KeyError:
            user_permissions = PERMISSION_PRIVATE
        else:
            user_permissions = Permission(user_permissions)
        
        
        self = object.__new__(cls)
        self.id = id_
        self.application_id = application_id
        self.type = type_
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.interaction = None
        self.token = token
        self.user = user
        self.user_permissions = user_permissions
        self._response_flag = RESPONSE_FLAG_NONE
        self._cached_users = None
        self.message = message
        
        # Cache our user if called from guild. This is required to kill references to the user in the guild.
        if (guild is not None):
            self._add_cached_user(user)
        
        # All field is set -> we can now create our own child
        interaction_type = INTERACTION_TYPE_TABLE.get(type_value, None)
        if (interaction_type is not None):
            self.interaction = interaction_type(data['data'], self)
        
        # Bind cached users to the guild for un-caching on object unallocation.
        cached_users = self._cached_users
        if (cached_users is not None):
            for user in cached_users:
                key = (user, guild)
                USER_GUILD_CACHE = cls._USER_GUILD_CACHE
                try:
                    reference_count = USER_GUILD_CACHE[key]
                except KeyError:
                    reference_count = 1
                else:
                    reference_count += 1
                
                USER_GUILD_CACHE[key] = reference_count
        
        return self
    
    
    async def wait_for_response_message(self, *, timeout=None):
        """
        Waits for response message. Applicable for application command interactions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        timeout : `None` or `float`, Optional (Keyword only)
            The maximal time to wait for message before `TimeoutError` is raised.
        
        Returns
        -------
        message : ``Message``
            The received message.
        
        Raises
        ------
        RuntimeError
            The interaction was acknowledged with `show_for_invoking_user_only=True` (as ephemeral). Response
            `message` cannot be detected.
        TimeoutError
            Message was not received before timeout.
        """
        message = self.message
        if (message is not None):
            return message
        
        if self._response_flag & RESPONSE_FLAG_EPHEMERAL:
            raise RuntimeError(f'The interaction was acknowledged with `show_for_invoking_user_only=True` '
                f'(as ephemeral). Response `message` cannot be detected.')
        
        try:
            waiter = INTERACTION_EVENT_MESSAGE_WAITERS[self]
        except KeyError:
            waiter = Future(KOKORO)
            INTERACTION_EVENT_MESSAGE_WAITERS[self] = waiter
        
        waiter = shield(waiter, KOKORO)
        
        if (timeout is not None):
            future_or_timeout(waiter, timeout)
        
        await waiter
        return self.message
    
    
    def __del__(self):
        """
        Unregisters the user-guild pair from the interaction cache.
        """
        cached_users = self._cached_users
        if cached_users is None:
            return
        
        guild = self.guild
        if (guild is None):
            return
        
        for user in cached_users:
            key = (user, guild)
            USER_GUILD_CACHE = self._USER_GUILD_CACHE
            
            # A client meanwhile joined the guild?
            if not guild.partial:
                try:
                    del USER_GUILD_CACHE[key]
                except KeyError:
                    pass
                return
            
            try:
                reference_count = USER_GUILD_CACHE[key]
            except KeyError:
                reference_count = 0
            else:
                if reference_count == 1:
                    del USER_GUILD_CACHE[key]
                    reference_count = 0
                else:
                    reference_count -= 1
            
            if reference_count == 0:
                try:
                    del user.guild_profiles[guild.id]
                except KeyError:
                    pass
    
    
    def __repr__(self):
        """Returns the representation of the event."""
        repr_parts = ['<', self.__class__.__name__]
        
        response_state_names = None
        response_state = self._response_flag
        
        if response_state == RESPONSE_FLAG_NONE:
            pass
        
        if response_state & RESPONSE_FLAG_DEFERRING:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('deferring')
        
        if response_state & RESPONSE_FLAG_DEFERRED:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('deferred')
        
        if response_state & RESPONSE_FLAG_RESPONDING:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('responding')
        
        if response_state & RESPONSE_FLAG_RESPONDED:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('responded')
        
        if response_state & RESPONSE_FLAG_EPHEMERAL:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('ephemeral')
        
        if (response_state_names is not None):
            repr_parts.append(' (')
            index = 0
            limit = len(response_state_names)
            while True:
                response_state_name = response_state_names[index]
                repr_parts.append(response_state_name)
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(response_state_name)
            repr_parts.append('),')
        
        repr_parts.append(' type=')
        interaction_type = self.type
        repr_parts.append(interaction_type.name)
        repr_parts.append(' (')
        repr_parts.append(repr(interaction_type.value))
        repr_parts.append(')')
        
        
        guild = self.guild
        if (guild is not None):
            repr_parts.append(', guild=')
            repr_parts.append(repr(guild))
        
        
        channel = self.channel
        if (channel is not None):
            repr_parts.append(', channel=')
            repr_parts.append(repr(channel))

        
        message = self.message
        if (message is not None):
            repr_parts.append(', message=')
            repr_parts.append(repr(message))
        
        
        repr_parts.append(', user=')
        repr_parts.append(repr(self.user))
        
        
        repr_parts.append(', interaction=')
        repr_parts.append(repr(self.interaction))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def is_unanswered(self):
        """
        Returns whether the event was not acknowledged and not acknowledging either.
        
        Returns
        -------
        is_unanswered : `bool`
        """
        return True if (self._response_flag == RESPONSE_FLAG_NONE) else False
    
    
    def is_acknowledging(self):
        """
        Returns whether the event is being acknowledged.
        
        Returns
        -------
        is_acknowledging : `bool`
        """
        return True if (self._response_flag & RESPONSE_FLAG_ACKNOWLEDGING) else False
    
    
    def is_acknowledged(self):
        """
        Returns whether the event is acknowledged.
        
        Returns
        -------
        is_acknowledged : `bool`
        """
        return True if (self._response_flag & RESPONSE_FLAG_ACKNOWLEDGED) else False
    
    
    def is_deferred(self):
        """
        Returns whether the event is deferred.
        
        Returns
        -------
        is_deferred : `bool`
        """
        response_state = self._response_flag
        if response_state & RESPONSE_FLAG_RESPONDED:
            return False
        
        if response_state & RESPONSE_FLAG_DEFERRED:
            return True
        
        return False
    
    
    def is_responding(self):
        """
        Returns whether the even it being responded.
        
        Returns
        -------
        is_responding : `bool`
        """
        return True if (self._response_flag & RESPONSE_FLAG_RESPONDING) else False
    
    
    def is_responded(self):
        """
        Returns whether was responded.
        
        Returns
        -------
        is_responded : `bool`
        """
        return True if (self._response_flag & RESPONSE_FLAG_RESPONDED) else False
    
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 3
    
    
    def __iter__(self):
        """
        Unpacks the event.
        
        This method is a generator.
        """
        yield self.type
        yield self.user
        yield self.interaction
    
    
    @property
    def channel(self):
        """
        Returns the interaction's event.
        
        Returns
        -------
        channel : ``ChannelTextBase``, `None`
        """
        return CHANNELS.get(self.channel_id, None)
    
    
    @property
    def guild(self):
        """
        Returns the interaction's guild.
        
        Returns
        -------
        guild : ``Guild``, `None`
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    @property
    def client(self):
        """
        Returns the interaction's client.
        
        Returns
        -------
        client : `Client`
        
        Raises
        ------
        RuntimeError
            Client could not be identified.
        """
        try:
            return APPLICATION_ID_TO_CLIENT[self.application_id]
        except KeyError:
            raise RuntimeError(f'Client of {self!r} could not be identified.') from None
    
    
    @property
    def voice_client(self):
        """
        Returns the voice client of the interaction's client in it's guild.
        
        Returns
        -------
        voice_client : `None` or ``VoiceClient``
        """
        try:
            client = APPLICATION_ID_TO_CLIENT[self.application_id]
        except KeyError:
            voice_client = None
        else:
            guild_id = self.message.guild_id
            if guild_id:
                voice_client = client.voice_clients.get(guild_id, None)
            else:
                voice_client = None
        
        return voice_client
    
    
    def _add_cached_user(self, user):
        """
        Adds a user to the cached ones by the interaction.
        
        This function might be called inside of ``InteractionEvent.__new__`` when initializing it's interaction.
        
        Parameters
        ----------
        user : ``ClientUserBase``
            The user to add to cache.
        """
        cached_users = self._cached_users
        if cached_users is None:
            self._cached_users = [user]
        else:
            if (user not in cached_users):
                cached_users.append(user)
    
    
    def _add_response_waiter(self):
        """
        Adds the interaction event to response waiters.
        
        Called when the interaction is application command one, to resolve it's ``.message`` attribute when created.
        """
        INTERACTION_EVENT_RESPONSE_WAITERS[self.id] = self
    

class InteractionResponseContext:
    """
    Interaction response context manager for managing the interaction's response flag.
    
    Attributes
    ----------
    interaction : ``InteractionEvent``
        The respective interaction event.
    is_deferring : `bool`
        Whether the request just deferring the interaction.
    is_ephemeral : `bool`
        Whether the request is ephemeral.
    """
    __slots__ = ('interaction', 'is_deferring', 'is_ephemeral',)
    
    def __new__(cls, interaction, is_deferring, is_ephemeral):
        """
        Creates a new ``InteractionResponseContext`` instance with the given parameters.
        
        Parameters
        ----------
        is_deferring : `bool`
            Whether the request just deferring the interaction.
        is_ephemeral : `bool`
            Whether the request is ephemeral.
        """
        self = object.__new__(cls)
        self.interaction = interaction
        self.is_deferring = is_deferring
        self.is_ephemeral = is_ephemeral
        return self
    
    def __enter__(self):
        """Enters the context manager as deferring or responding if applicable."""
        interaction = self.interaction
        response_flag = interaction._response_flag
        
        if self.is_deferring:
            if not (response_flag&RESPONSE_FLAG_ACKNOWLEDGING_OR_ACKNOWLEDGED):
                response_flag |= RESPONSE_FLAG_DEFERRING
        else:
            if (not response_flag&RESPONSE_FLAG_RESPONDING_OR_RESPONDED) and \
                    (not response_flag&RESPONSE_FLAG_DEFERRING_OR_DEFERRED):
                response_flag |= RESPONSE_FLAG_RESPONDING
        
        interaction._response_flag = response_flag
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exits the context manager, marking the interaction as deferred or responded if no exception occurred."""
        interaction = self.interaction
        response_flag = interaction._response_flag
        if exc_type is None:
            if self.is_ephemeral:
                if not response_flag&RESPONSE_FLAG_ACKNOWLEDGED:
                    response_flag ^= RESPONSE_FLAG_EPHEMERAL
            
            if self.is_deferring:
                if response_flag&RESPONSE_FLAG_DEFERRING:
                    response_flag ^= RESPONSE_FLAG_DEFERRING
                    response_flag |= RESPONSE_FLAG_DEFERRED
            else:
                if response_flag&RESPONSE_FLAG_RESPONDING:
                    response_flag ^= RESPONSE_FLAG_RESPONDING
                    response_flag |= RESPONSE_FLAG_RESPONDED
        
        else:
            if self.is_deferring:
                if response_flag&RESPONSE_FLAG_DEFERRING:
                    response_flag ^= RESPONSE_FLAG_DEFERRING
            else:
                if response_flag&RESPONSE_FLAG_RESPONDING:
                    response_flag ^= RESPONSE_FLAG_RESPONDING
        
        interaction._response_flag = response_flag
        return False
