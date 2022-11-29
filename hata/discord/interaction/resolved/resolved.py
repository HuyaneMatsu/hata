__all__ = ('Resolved',)

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_attachments, parse_channels, parse_messages, parse_roles, parse_users, put_attachments_into,
    put_channels_into, put_messages_into, put_roles_into, put_users_into, validate_attachments, validate_channels,
    validate_messages, validate_roles, validate_users
)


class Resolved(RichAttributeErrorBaseType):
    """
    Contains the resolved entities by an interaction.
    
    Attributes
    ----------
    attachments : `None`, `dict` of (`int`, `Attachment``) items
        Resolved received attachments stored by their identifier as keys if any.
    
    channels : `None`, `dict` of (`int`, ``Channel``) items
        Resolved received channels stored by their identifier as keys if any.
    
    roles : `None`, `dict` of (`int`, ``Role``) items
        Resolved received roles stored by their identifier as keys if any.
    
    messages : `None`, `dict` of (`int`, ``Message``) items
        Resolved received messages stored by their identifier as keys if any.
    
    users : `None`, `dict` of (`int`, ``ClientUserBase``) items
        Resolved received users stored by their identifier as keys if any.
    """
    __slots__ = ('attachments', 'channels', 'roles', 'messages', 'users')
    
    def __new__(cls, *, attachments = None, channels = None, roles = None, messages = None, users = None):
        """
        Creates a new resolved object.
        
        Parameters
        ----------
        attachments : `None`, `dict` of (`int`, `Attachment``) items = `None`, Optional (Keyword only)
            Resolved received attachments stored by their identifier as keys if any.
        
        channels : `None`, `dict` of (`int`, ``Channel``) items = `None`, Optional (Keyword only)
            Resolved received channels stored by their identifier as keys if any.
        
        roles : `None`, `dict` of (`int`, ``Role``) items = `None`, Optional (Keyword only)
            Resolved received roles stored by their identifier as keys if any.
        
        messages : `None`, `dict` of (`int`, ``Message``) items = `None`, Optional (Keyword only)
            Resolved received messages stored by their identifier as keys if any.
        
        users : `None`, `dict` of (`int`, ``ClientUserBase``) items = `None`, Optional (Keyword only)
            Resolved received users stored by their identifier as keys if any.
        
        Raises
        ------
        TypeError
            - Parameter of incorrect type given.
        ValueError
            - Parameter of incorrect value given.
        """
        attachments = validate_attachments(attachments)
        channels = validate_channels(channels)
        roles = validate_roles(roles)
        messages = validate_messages(messages)
        users = validate_users(users)
        
        # Construct
        self = object.__new__(cls)
        self.attachments = attachments
        self.channels = channels
        self.roles = roles
        self.messages = messages
        self.users = users
        return self
    
    
    @classmethod
    def from_data(cls, data, interaction_event):
        """
        Creates a new resolved instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Resolved data.
        
        interaction_event : ``InteractionEvent``
            The parent interaction event.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.attachments = parse_attachments(data)
        self.channels = parse_channels(data, interaction_event)
        self.roles = parse_roles(data, interaction_event)
        self.messages = parse_messages(data)
        self.users = parse_users(data, interaction_event)
        return self
    
    
    def to_data(self, *, defaults = False, interaction_event = None):
        """
        Converts the resolved instance into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included as well.
        
        interaction_event : ``InteractionEvent`` = `None`, Optional (Keyword only)
            The respective guild's identifier to use for handing user guild profiles.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_attachments_into(self.attachments, data, defaults)
        put_channels_into(self.channels, data, defaults)
        put_roles_into(self.roles, data, defaults)
        put_messages_into(self.messages, data, defaults)
        put_users_into(self.users, data, defaults, interaction_event = interaction_event)
        return data
    
    
    def copy(self):
        """
        Copies the resolved instance.
        
        Returns
        -------
        new : `instance<type<cls>``
        """
        # attachments
        attachments = self.attachments
        if (attachments is not None):
            attachments = attachments.copy()
        
        # channels
        channels = self.channels
        if (channels is not None):
            channels = channels.copy()
        
        # roles
        roles = self.roles
        if (roles is not None):
            roles = roles.copy()
        
        # messages
        messages = self.messages
        if (messages is not None):
            messages = messages.copy()
        
        # users
        users = self.users
        if (users is not None):
            users = users.copy()
        
        # Construct
        new = object.__new__(type(self))
        new.attachments = attachments
        new.channels = channels
        new.roles = roles
        new.messages = messages
        new.users = users
        return new
    
    
    def copy_with(self, *, attachments = ..., channels = ..., roles = ..., messages = ..., users = ...):
        """
        Copies the resolved with the specified fields.
        
        Parameters
        ----------
        attachments : `None`, `dict` of (`int`, `Attachment``) items, Optional (Keyword only)
            Resolved received attachments stored by their identifier as keys if any.
        
        channels : `None`, `dict` of (`int`, ``Channel``) items, Optional (Keyword only)
            Resolved received channels stored by their identifier as keys if any.
        
        roles : `None`, `dict` of (`int`, ``Role``) items, Optional (Keyword only)
            Resolved received roles stored by their identifier as keys if any.
        
        messages : `None`, `dict` of (`int`, ``Message``) items, Optional (Keyword only)
            Resolved received messages stored by their identifier as keys if any.
        
        users : `None`, `dict` of (`int`, ``ClientUserBase``) items, Optional (Keyword only)
            Resolved received users stored by their identifier as keys if any.
        
        Raises
        ------
        TypeError
            - Parameter of incorrect type given.
        ValueError
            - Parameter of incorrect value given.
        """
        # attachments
        if attachments is ...:
            attachments = self.attachments
            if (attachments is not None):
                attachments = attachments.copy()
        else:
            attachments = validate_attachments(attachments)
        
        # channels
        if channels is ...:
            channels = self.channels
            if (channels is not None):
                channels = channels.copy()
        else:
            channels = validate_channels(channels)
        
        # roles
        if roles is ...:
            roles = self.roles
            if (roles is not None):
                roles = roles.copy()
        else:
            roles = validate_roles(roles)
        
        # messages
        if messages is ...:
            messages = self.messages
            if (messages is not None):
                messages = messages.copy()
        else:
            messages = validate_messages(messages)
        
        # users
        if users is ...:
            users = self.users
            if (users is not None):
                users = users.copy()
        else:
            users = validate_users(users)
        
        # Construct
        new = object.__new__(type(self))
        new.attachments = attachments
        new.channels = channels
        new.roles = roles
        new.messages = messages
        new.users = users
        return new
    
    
    def __repr__(self):
        """Returns the resolved's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        for field_name, field_value in zip(
            ('attachments', 'channels', 'roles', 'messages', 'users'), self._iter_entity_containers(),
        ):
            if (field_value is not None):
                if field_added:
                    repr_parts.append(',')
                else:
                    field_added = True
                
                repr_parts.append(' ')
                repr_parts.append(field_name)
                repr_parts.append('=')
                repr_parts.append(repr(field_value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two resolved are equal."""
        if type(other) is not type(self):
            return NotImplemented
        
        for self_container, other_container in zip(self._iter_entity_containers(), other._iter_entity_containers()):
            if self_container != other_container:
                return False
        
        return True
    
    
    def __hash__(self):
        """Returns the resolved's hash value."""
        hash_value = 0
        
        shift = 0
        
        for field_value in self._iter_entity_containers():
            if (field_value is not None):
                hash_value ^= len(field_value) << shift
                
                for entity_id in field_value.keys():
                    hash_value ^= entity_id
            
            shift += 4
        
        return hash_value
    
    
    def _iter_entity_containers(self):
        """
        Iterates over the entity containers of the resolved instance.
        
        This method is an iterable generator.
        
        Yields
        ------
        container : `None`, `dict` of (`str`, `object`) items
        """
        yield self.attachments
        yield self.channels
        yield self.roles
        yield self.messages
        yield self.users
    
    # Extra utility
    
    def resolve_attachment(self, attachment_id):
        """
        Tries to resolve an attachment by the given identifier.
        
        Parameters
        ----------
        attachment_id : `int`
            Attachment identifier.
        
        Returns
        -------
        attachment : `None`, ``Attachment``
        """
        attachments = self.attachments
        if (attachments is not None):
            return attachments.get(attachment_id, None)
    
    
    def resolve_channel(self, channel_id):
        """
        Tries to resolve an channel by the given identifier.
        
        Parameters
        ----------
        channel_id : `int`
            Channel identifier.
        
        Returns
        -------
        channel : `None`, ``Channel``
        """
        channels = self.channels
        if (channels is not None):
            return channels.get(channel_id, None)
    
    
    def resolve_role(self, role_id):
        """
        Tries to resolve an role by the given identifier.
        
        Parameters
        ----------
        role_id : `int`
            Role identifier.
        
        Returns
        -------
        role : `None`, ``Role``
        """
        roles = self.roles
        if (roles is not None):
            return roles.get(role_id, None)
    
    
    def resolve_message(self, message_id):
        """
        Tries to resolve an message by the given identifier.
        
        Parameters
        ----------
        message_id : `int`
            Message identifier.
        
        Returns
        -------
        message : `None`, ``Message``
        """
        messages = self.messages
        if (messages is not None):
            return messages.get(message_id, None)
    
    
    def resolve_user(self, user_id):
        """
        Tries to resolve an user by the given identifier.
        
        Parameters
        ----------
        user_id : `int`
            User identifier.
        
        Returns
        -------
        user : `None`, ``ClientUserBase``
        """
        users = self.users
        if (users is not None):
            return users.get(user_id, None)
    
    
    def resolve_mentionable(self, mentionable_id):
        """
        Tries to resolve a mentionable entity (user / role).
        
        Parameters
        ----------
        mentionable_id : `int`
            Entity identifier.
        
        Returns
        -------
        entity : `None`, ``Role``, ``ClientUserBase``
        """
        users = self.users
        if (users is not None):
            try:
                return users[mentionable_id]
            except KeyError:
                pass
        
        roles = self.roles
        if (roles is not None):
            try:
                return roles[mentionable_id]
            except KeyError:
                pass
    
    
    def resolve_entity(self, entity_id):
        """
        Tries to resolve any entity with the given identifier.
        
        Parameters
        ----------
        entity_id : `int`
            Entity identifier.
        
        Returns
        -------
        entity : `None` ``Attachment``, ``Channel``, ``ClientUserBase``, ``Role``, ``Message``
        """
        for container in self._iter_entity_containers():
            if (container is not None):
                try:
                    return container[entity_id]
                except KeyError:
                    pass
