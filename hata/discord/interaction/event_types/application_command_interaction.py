__all__ = ('ApplicationCommandInteraction', 'ApplicationCommandInteractionOption')

from scarletio import copy_docs

from ...bases import DiscordEntity
from ...channel import create_partial_channel_from_data
from ...message import Attachment, Message
from ...role import Role
from ...user import User

from ..preinstanced import ApplicationCommandOptionType

from .interaction_field_base import InteractionFieldBase


class ApplicationCommandInteraction(DiscordEntity, InteractionFieldBase):
    """
    Represents an ``ApplicationCommand`` invoked by a user.
    
    Attributes
    ----------
    id : `int`
        The represented application command's identifier number.
    name : `str`
        The name of the command. It's length can be in range [1:32].
    options : `None`, `tuple` of ``ApplicationCommandInteractionOption``
        The parameters and values from the user if any. Defaults to `None` if non is received.
    resolved_attachments : `None`, `dict` of (`int`, `Attachment``) items
        Resolved received attachments stored by their identifier as keys if any.
    resolved_channels : `None`, `dict` of (`int`, ``ChannelBase``) items
        Resolved received channels stored by their identifier as keys if any.
    resolved_roles : `None`, `dict` of (`int`, ``Role``) items
        Resolved received roles stored by their identifier as keys if any.
    resolved_messages : `None`, `dict` of (`int`, ``Message``) items
        Resolved received messages stored by their identifier as keys if any.
    resolved_users : `None`, `dict` of (`int`, ``ClientUserBase``) items
        Resolved received users stored by their identifier as keys if any.
    target_id : `int`
        The interaction's target's identifier.
    """
    __slots__ = (
        'name', 'options', 'resolved_attachments', 'resolved_channels', 'resolved_roles', 'resolved_messages',
        'resolved_users', 'target_id'
    )
    
    
    @copy_docs(InteractionFieldBase.__eq__)
    def __new__(cls, data, interaction_event):
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
            resolved_attachments = None
            resolved_channels = None
            resolved_roles = None
            resolved_messages = None
            resolved_users = None
        else:
            # resolved_attachments
            try:
                resolved_attachment_datas = resolved_data['attachments']
            except KeyError:
                resolved_attachments = None
            else:
                if resolved_attachment_datas:
                    resolved_attachments = {}
                    
                    for attachment_data in resolved_attachment_datas.values():
                        attachment = Attachment(attachment_data)
                        if (attachment is not None):
                            resolved_attachments[attachment.id] = attachment
                    
                    if not resolved_attachments:
                        resolved_attachments = None
                else:
                    resolved_attachments = None
            
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
        self.resolved_attachments = resolved_attachments
        self.resolved_users = resolved_users
        self.resolved_channels = resolved_channels
        self.resolved_roles = resolved_roles
        self.resolved_messages = resolved_messages
        self.target_id = target_id
        
        interaction_event._add_response_waiter()
        
        return self
    
    
    @copy_docs(InteractionFieldBase.__repr__)
    def __repr__(self):
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
    
    
    @copy_docs(InteractionFieldBase.__eq__)
    def __eq__(self, other):
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
        
        # resolved_attachments
        if self.resolved_attachments != other.resolved_attachments:
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
    
    
    @copy_docs(InteractionFieldBase.__hash__)
    def __hash__(self):
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
        
        # resolved_attachments
        resolved_attachments = self.resolved_attachments
        if (resolved_attachments is not None):
            hash_value ^= (len(resolved_attachments) << 24)
            
            for attachment_id in resolved_attachments.keys():
                hash_value ^= attachment_id
        
        # resolved_channels
        resolved_channels = self.resolved_channels
        if (resolved_channels is not None):
            hash_value ^= (len(resolved_channels) << 8)
            
            for channel_id in resolved_channels.keys():
                hash_value ^= channel_id
        
        # resolved_roles
        resolved_roles = self.resolved_roles
        if (resolved_roles is not None):
            hash_value ^= (len(resolved_roles) << 12)
            
            for role_id in resolved_roles.keys():
                hash_value ^= role_id
        
        # resolved_messages
        resolved_messages = self.resolved_messages
        if (resolved_messages is not None):
            hash_value ^= (len(resolved_messages) << 16)
            
            for message_id in resolved_messages.keys():
                hash_value ^= message_id
        
        # resolved_users
        resolved_users = self.resolved_users
        if (resolved_users is not None):
            hash_value ^= (len(resolved_users) << 20)
            
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
        resolved : `None`, ``DiscordEntity``
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
        
        
        resolved_attachments = self.resolved_attachments
        if (resolved_attachments is not None):
            try:
                entity = resolved_attachments[entity_id]
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
    
    options : `None`, `tuple` of ``ApplicationCommandInteractionOption``
        The parameters and values from the user. Present if a sub-command was used. Defaults to `None` if non is
        received.
        
        Mutually exclusive with the `value` field.
    
    type : ``ApplicationCommandOptionType``
        The option's type.
    
    value : `None`, `str`, `bool`, `float`, `int`
        The given value by the user.
        
        Mutually exclusive with the `options` field,
    
    """
    __slots__ = ('name', 'options', 'type', 'value')
    
    def __new__(cls, data):
        """
        Creates a new ``ApplicationCommandInteractionOption`` from the data received from Discord.
        
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
        hash_value ^= (self.type.value << 8)
        
        # value
        value = self.value
        if (value is not None):
            hash_value ^= hash(value)
        
        return hash_value
