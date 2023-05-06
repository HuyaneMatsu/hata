__all__ = ('Connection', )

from scarletio import include

from ...bases import DiscordEntity
from ...precreate_helpers import process_precreate_parameters_and_raise_extra

from .fields import (
    parse_friend_sync, parse_id, parse_integrations, parse_metadata_visibility, parse_name, parse_revoked,
    parse_show_activity, parse_two_way_link, parse_type, parse_verified, parse_visibility, put_friend_sync_into,
    put_id_into, put_integrations_into, put_metadata_visibility_into, put_name_into, put_revoked_into,
    put_show_activity_into, put_two_way_link_into, put_type_into, put_verified_into, put_visibility_into,
    validate_friend_sync, validate_id, validate_integrations, validate_metadata_visibility, validate_name,
    validate_revoked, validate_show_activity, validate_two_way_link, validate_type, validate_verified,
    validate_visibility
)
from .preinstanced import ConnectionType, ConnectionVisibility


Integration = include('Integration')

PRECREATE_FIELDS = {
    'connection_type': ('type', validate_type),
    'friend_sync': ('friend_sync', validate_friend_sync),
    'integrations': ('integrations', validate_integrations),
    'metadata_visibility': ('metadata_visibility', validate_metadata_visibility),
    'name': ('name', validate_name),
    'revoked': ('revoked', validate_revoked),
    'show_activity': ('show_activity', validate_show_activity),
    'two_way_link': ('two_way_link', validate_two_way_link),
    'verified': ('verified', validate_verified),
    'visibility': ('visibility', validate_visibility),
}


class Connection(DiscordEntity):
    """
    A connection object that a user is attached to.
    
    Attributes
    ----------
    friend_sync : `bool`
        Whether the user has friend sync enabled for the connection.
    
    id : `int`
        The unique identifier value of the connection.
    
    integrations : `None` or `tuple` of ``Integration``
        A guild's integrations which are attached to the connection.
    
    metadata_visibility : ``ConnectionVisibility``
        For who is the connection metadata visible for.
    
    name : `str`
        The username of the connected account.
    
    revoked : `bool`
        Whether the connection is revoked.
    
    show_activity : `bool`
        Whether activity related to this connection will be shown in presence updates.
    
    two_way_link : `bool`
         Whether this connection has a corresponding third party OAuth2 token.
    
    type : ``ConnectionType``
        The service of the connection.
    
    verified : `bool`
        Whether the connection is verified.
    
    visibility : ``ConnectionVisibility``
        For who is the connection visible for.
    """
    __slots__ = (
        'friend_sync', 'integrations', 'metadata_visibility', 'name', 'revoked', 'show_activity', 'two_way_link',
        'type', 'verified', 'visibility'
    )
    
    
    def __new__(
        cls,
        *,
        connection_type = ...,
        friend_sync = ...,
        integrations = ...,
        metadata_visibility = ...,
        name = ...,
        revoked = ...,
        show_activity = ...,
        two_way_link = ...,
        verified = ...,
        visibility = ...,
    ):
        """
        Creates a new connection from the given parameters.
        
        Parameters
        ----------
        connection_type : ``ConnectionType``, `str`, Optional (Keyword only)
            The service of the connection.
        
        friend_sync : `bool`, Optional (Keyword only)
            Whether the user has friend sync enabled for the connection.
        
        integrations : `None` or `iterable` of ``Integration``, Optional (Keyword only)
            A guild's integrations which are attached to the connection.
        
        metadata_visibility : ``ConnectionVisibility``, `int`, Optional (Keyword only)
            For who is the connection metadata visible for.
        
        name : `str`, Optional (Keyword only)
            The username of the connected account.
        
        revoked : `bool`, Optional (Keyword only)
            Whether the connection is revoked.
        
        show_activity : `bool`, Optional (Keyword only)
            Whether activity related to this connection will be shown in presence updates.
        
        two_way_link : `bool`, Optional (Keyword only)
             Whether this connection has a corresponding third party OAuth2 token.
        
        verified : `bool`, Optional (Keyword only)
            Whether the connection is verified.
        
        visibility : ``ConnectionVisibility``, `int`, Optional (Keyword only)
            For who is the connection visible for.
        
        Raises
        ------
        TypeError
            - If a field's type is unacceptable.
        ValueError
            - If a a field's value is unacceptable.
        """
        # connection_type
        if connection_type is ...:
            connection_type = ConnectionType.unknown
        else:
            connection_type = validate_type(connection_type)
        
        # friend_sync
        if friend_sync is ...:
            friend_sync = False
        else:
            friend_sync = validate_friend_sync(friend_sync)
        
        # integrations
        if integrations is ...:
            integrations = None
        else:
            integrations = validate_integrations(integrations)
        
        # metadata_visibility
        if metadata_visibility is ...:
            metadata_visibility = ConnectionVisibility.user_only
        else:
            metadata_visibility = validate_metadata_visibility(metadata_visibility)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # revoked
        if revoked is ...:
            revoked = False
        else:
            revoked = validate_revoked(revoked)
        
        # show_activity
        if show_activity is ...:
            show_activity = False
        else:
            show_activity = validate_show_activity(show_activity)
        
        # two_way_link
        if two_way_link is ...:
            two_way_link = False
        else:
            two_way_link = validate_two_way_link(two_way_link)
        
        # verified
        if verified is ...:
            verified = False
        else:
            verified = validate_verified(verified)
        
        # visibility
        if visibility is ...:
            visibility = ConnectionVisibility.user_only
        else:
            visibility = validate_visibility(visibility)
        
        # Construct
        self = object.__new__(cls)
        
        self.id = 0
        self.friend_sync = friend_sync
        self.integrations = integrations
        self.metadata_visibility = metadata_visibility
        self.name = name
        self.revoked = revoked
        self.show_activity = show_activity
        self.two_way_link = two_way_link
        self.type = connection_type
        self.verified = verified
        self.visibility = visibility
        
        return self
    
    
    @classmethod
    def precreate(cls, connection_id, **keyword_parameters):
        """
        Creates a new connection with the given predefined fields.
        
        > Since connections are not cached globally, this method is only be used for testing.
        
        Parameters
        ----------
        connection_id : `int`
            The connection's identifier.
        **keyword_parameters : Keyword Parameters
            The attributes to set.
        
        Other Parameters
        ----------------
        connection_type : ``ConnectionType``, `str`, Optional (Keyword only)
            The service of the connection.
        
        friend_sync : `bool`, Optional (Keyword only)
            Whether the user has friend sync enabled for the connection.
        
        integrations : `None` or `iterable` of ``Integration``, Optional (Keyword only)
            A guild's integrations which are attached to the connection.
        
        metadata_visibility : ``ConnectionVisibility``, `int`, Optional (Keyword only)
            For who is the connection metadata visible for.
        
        name : `str`, Optional (Keyword only)
            The username of the connected account.
        
        revoked : `bool`, Optional (Keyword only)
            Whether the connection is revoked.
        
        show_activity : `bool`, Optional (Keyword only)
            Whether activity related to this connection will be shown in presence updates.
        
        two_way_link : `bool`, Optional (Keyword only)
             Whether this connection has a corresponding third party OAuth2 token.
        
        verified : `bool`, Optional (Keyword only)
            Whether the connection is verified.
        
        visibility : ``ConnectionVisibility``, `int`, Optional (Keyword only)
            For who is the connection visible for.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If `connection_id` is not `int`.
            - If a field's type is unacceptable.
            - Extra or unused parameters
        ValueError
            - If a a field's value is unacceptable.
        """
        connection_id = validate_id(connection_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        self = cls._create_empty(connection_id)
        
        if (processed is not None):
            for name, value in processed:
                setattr(self, name, value)
        
        return self
    
    
    @classmethod
    def _create_empty(cls, connection_id):
        """
        Creates a new connection with it's default attributes set.
        
        Parameters
        ----------
        connection_id : `int`
            The connection's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        
        self.id = connection_id
        self.friend_sync = False
        self.integrations = None
        self.metadata_visibility = ConnectionVisibility.user_only
        self.name = ''
        self.revoked = False
        self.show_activity = False
        self.two_way_link = False
        self.type = ConnectionType.unknown
        self.verified = False
        self.visibility = ConnectionVisibility.user_only
        
        return self
    
    
    def __repr__(self):
        """Returns the connection's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        connection_id = self.id
        if connection_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(connection_id))
        
        else:
            repr_parts.append(' (partial)')
        
        connection_type = self.type
        if (connection_type is not ConnectionType.unknown):
            repr_parts.append(', type = ')
            repr_parts.append(connection_type.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(connection_type.value))
        
        name = self.name
        if name:
            repr_parts.append(', name = ')
            repr_parts.append(repr(name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    def __hash__(self):
        """Returns the connection's hash."""
        connection_id = self.id
        if connection_id:
            return connection_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Returns a partial connection's hash value.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # friend_sync
        hash_value ^= self.friend_sync
        
        # id | Internal -> skip
        
        # integrations
        integrations = self.integrations
        if (integrations is not None):
            hash_value ^= len(integrations) << 1
            for integration in integrations:
                hash_value ^= hash(integration)
        
        # metadata_visibility
        hash_value ^= hash(self.metadata_visibility) << 5
        
        # name
        hash_value ^= hash(self.name)
        
        # revoked
        hash_value ^= self.revoked << 9
        
        # show_activity
        hash_value ^= self.show_activity << 10
        
        # two_way_link
        hash_value ^= self.two_way_link << 11
        
        # type
        hash_value ^= hash(self.type)
        
        # verified
        hash_value ^= self.verified << 12
        
        # visibility
        hash_value ^= hash(self.visibility) << 13
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two connections are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two connections are equal."""
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
        if self_id and other_id:
            if self_id == other_id:
                return True
            
            return False
        
        # friend_sync
        if self.friend_sync != other.friend_sync:
            return False
        
        # integrations
        if self.integrations != other.integrations:
            return False
        
        # metadata_visibility
        if self.metadata_visibility is not other.metadata_visibility:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # revoked
        if self.revoked != other.revoked:
            return False
        
        # show_activity
        if self.show_activity != other.show_activity:
            return False
        
        # two_way_link
        if self.two_way_link != other.two_way_link:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        # verified
        if self.verified != other.verified:
            return False
        
        # visibility
        if self.visibility is not other.visibility:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a connection object from received connection data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`)
            Received connection data.
        """
        self = object.__new__(cls)
        
        self.id = parse_id(data)
        self.friend_sync = parse_friend_sync(data)
        self.integrations = parse_integrations(data)
        self.metadata_visibility = parse_metadata_visibility(data)
        self.name = parse_name(data)
        self.revoked = parse_revoked(data)
        self.show_activity = parse_show_activity(data)
        self.two_way_link = parse_two_way_link(data)
        self.type = parse_type(data)
        self.verified = parse_verified(data)
        self.visibility = parse_visibility(data)
        
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the connection to json serializable representation dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether we want to include identifiers as well.
        
        Returns
        -------
        data : `dict` of (`str`, `str`) items
        """
        data = {}
        
        if include_internals:
            put_id_into(self.id, data, defaults)
        
        put_friend_sync_into(self.friend_sync, data, defaults)
        put_integrations_into(self.integrations, data, defaults, include_internals = include_internals)
        put_metadata_visibility_into(self.metadata_visibility, data, defaults)
        put_name_into(self.name, data, defaults)
        put_revoked_into(self.revoked, data, defaults)
        put_show_activity_into(self.show_activity, data, defaults)
        put_two_way_link_into(self.two_way_link, data, defaults)
        put_type_into(self.type, data, defaults)
        put_verified_into(self.verified, data, defaults)
        put_visibility_into(self.visibility, data, defaults)
        
        return data
    
    
    def iter_integrations(self):
        """
        Iterates over the integrations of the connection.
        
        This method is an iterable generator.
        
        Yields
        ------
        integration : ``Integration``
        """
        integrations = self.integrations
        if (integrations is not None):
            yield from integrations
    
    
    def copy(self):
        """
        Copies the connection returning a new partial one.
        
        Returns
        -------
        new : `instance<cls>`
        """
        # Construct
        new = object.__new__(type(self))
        new.id = 0
        new.friend_sync = self.friend_sync
        integrations = self.integrations
        if (integrations is not None):
            integrations = (*integrations,)
        new.integrations = integrations
        new.metadata_visibility = self.metadata_visibility
        new.name = self.name
        new.revoked = self.revoked
        new.show_activity = self.show_activity
        new.two_way_link = self.two_way_link
        new.type = self.type
        new.verified = self.verified
        new.visibility = self.visibility
        return new

    
    def copy_with(
        self,
        *,
        connection_type = ...,
        friend_sync = ...,
        integrations = ...,
        metadata_visibility = ...,
        name = ...,
        revoked = ...,
        show_activity = ...,
        two_way_link = ...,
        verified = ...,
        visibility = ...,):
        """
        Copies the connection with the given fields returning a new partial one.
        
        Parameters
        ----------
        connection_type : ``ConnectionType``, `str`, Optional (Keyword only)
            The service of the connection.
        
        friend_sync : `bool`, Optional (Keyword only)
            Whether the user has friend sync enabled for the connection.
        
        integrations : `None` or `iterable` of ``Integration``, Optional (Keyword only)
            A guild's integrations which are attached to the connection.
        
        metadata_visibility : ``ConnectionVisibility``, `int`, Optional (Keyword only)
            For who is the connection metadata visible for.
        
        name : `str`, Optional (Keyword only)
            The username of the connected account.
        
        revoked : `bool`, Optional (Keyword only)
            Whether the connection is revoked.
        
        show_activity : `bool`, Optional (Keyword only)
            Whether activity related to this connection will be shown in presence updates.
        
        two_way_link : `bool`, Optional (Keyword only)
             Whether this connection has a corresponding third party OAuth2 token.
        
        verified : `bool`, Optional (Keyword only)
            Whether the connection is verified.
        
        visibility : ``ConnectionVisibility``, `int`, Optional (Keyword only)
            For who is the connection visible for.
        
        Raises
        ------
        TypeError
            - If a field's type is unacceptable.
        ValueError
            - If a a field's value is unacceptable.
        
        Returns
        -------
        new : `instance<cls>`
        """
        # connection_type
        if connection_type is ...:
            connection_type = self.type
        else:
            connection_type = validate_type(connection_type)
        
        # friend_sync
        if friend_sync is ...:
            friend_sync = self.friend_sync
        else:
            friend_sync = validate_friend_sync(friend_sync)
        
        # integrations
        if integrations is ...:
            integrations = self.integrations
            if (integrations is not None):
                integrations = (*integrations,)
        else:
            integrations = validate_integrations(integrations)
        
        # metadata_visibility
        if metadata_visibility is ...:
            metadata_visibility = self.metadata_visibility
        else:
            metadata_visibility = validate_metadata_visibility(metadata_visibility)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # revoked
        if revoked is ...:
            revoked = self.revoked
        else:
            revoked = validate_revoked(revoked)
        
        # show_activity
        if show_activity is ...:
            show_activity = self.show_activity
        else:
            show_activity = validate_show_activity(show_activity)
        
        # two_way_link
        if two_way_link is ...:
            two_way_link = self.two_way_link
        else:
            two_way_link = validate_two_way_link(two_way_link)
        
        # verified
        if verified is ...:
            verified = self.verified
        else:
            verified = validate_verified(verified)
        
        # visibility
        if visibility is ...:
            visibility = self.visibility
        else:
            visibility = validate_visibility(visibility)
        
        # Construct
        new = object.__new__(type(self))
        new.id = 0
        new.friend_sync = friend_sync
        integrations = integrations
        new.integrations = integrations
        new.metadata_visibility = metadata_visibility
        new.name = name
        new.revoked = revoked
        new.show_activity = show_activity
        new.two_way_link = two_way_link
        new.type = connection_type
        new.verified = verified
        new.visibility = visibility
        return new
