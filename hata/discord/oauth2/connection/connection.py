__all__ = ('Connection', )

from scarletio import include

from ...bases import DiscordEntity
from ...preconverters import preconvert_snowflake

from .fields import (
    parse_friend_sync, parse_integrations, parse_name, parse_revoked, parse_show_activity, parse_two_way_link,
    parse_type, parse_verified, parse_visibility, put_friend_sync_into, put_integrations_into, put_name_into,
    put_revoked_into, put_show_activity_into, put_two_way_link_into, put_type_into, put_verified_into,
    put_visibility_into, validate_friend_sync, validate_integrations, validate_name, validate_revoked,
    validate_show_activity, validate_two_way_link, validate_type, validate_verified, validate_visibility
)
from .preinstanced import ConnectionType, ConnectionVisibility


Integration = include('Integration')


class Connection(DiscordEntity):
    """
    A connection object that a user is attached to.
    
    Attributes
    ----------
    id : `int`
        The unique identifier value of the connection.
    
    friend_sync : `bool`
        Whether the user has friend sync enabled for the connection.
    
    integrations : `None` or `tuple` of ``Integration``
        A guild's integrations which are attached to the connection.
    
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
        'friend_sync', 'integrations', 'name', 'revoked', 'show_activity', 'two_way_link', 'type', 'verified',
        'visibility'
    )
    
    
    def __new__(cls, **keyword_parameters):
        """
        Creates a new connection from the given parameters.
        
        Parameters
        ----------
        **keyword_parameters : Keyword Parameters
            The attributes to set.
        
        Other Parameters
        ----------------
        friend_sync : `bool`, Optional (Keyword only)
            Whether the user has friend sync enabled for the connection.
        
        integrations : `None` or `iterable` of ``Integration``, Optional (Keyword only)
            A guild's integrations which are attached to the connection.
        
        name : `str`, Optional (Keyword only)
            The username of the connected account.
        
        revoked : `bool`, Optional (Keyword only)
            Whether the connection is revoked.
        
        show_activity : `bool`, Optional (Keyword only)
            Whether activity related to this connection will be shown in presence updates.
        
        two_way_link : `bool`, Optional (Keyword only)
             Whether this connection has a corresponding third party OAuth2 token.
        
        type : ``ConnectionType``, `str`, Optional (Keyword only)
            The service of the connection.
        
        verified : `bool`, Optional (Keyword only)
            Whether the connection is verified.
        
        visibility : ``ConnectionVisibility``, `int`, Optional (Keyword only)
            For who is the connection visible for.
        
        Raises
        ------
        TypeError
            - If a field's type is unacceptable.
            - Extra or unused parameters
        ValueError
            - If a a field's value is unacceptable.
        """
        self = cls._create_empty(0)
        self._set_attributes_from_keyword_parameters(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused parameters: {keyword_parameters!r}.'
            )
        
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
        friend_sync : `bool`, Optional (Keyword only)
            Whether the user has friend sync enabled for the connection.
        
        integrations : `None` or `iterable` of ``Integration``, Optional (Keyword only)
            A guild's integrations which are attached to the connection.
        
        name : `str`, Optional (Keyword only)
            The username of the connected account.
        
        revoked : `bool`, Optional (Keyword only)
            Whether the connection is revoked.
        
        show_activity : `bool`, Optional (Keyword only)
            Whether activity related to this connection will be shown in presence updates.
        
        two_way_link : `bool`, Optional (Keyword only)
             Whether this connection has a corresponding third party OAuth2 token.
        
        type : ``ConnectionType``, `str`, Optional (Keyword only)
            The service of the connection.
        
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
        connection_id = preconvert_snowflake(connection_id, 'connection_id')
        self = cls._create_empty(connection_id)
        self._set_attributes_from_keyword_parameters(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused parameters: {keyword_parameters!r}.'
            )
        
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
            repr_parts.append(' id=')
            repr_parts.append(repr(connection_id))
        
        else:
            repr_parts.append(' (partial)')
        
        connection_type = self.type
        if (connection_type is not ConnectionType.unknown):
            repr_parts.append(', type=')
            repr_parts.append(connection_type.name)
            repr_parts.append('~')
            repr_parts.append(repr(connection_type.value))
        
        name = self.name
        if name:
            repr_parts.append(', name=')
            repr_parts.append(repr(name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
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
        
        self.id = int(data['id'])
        self.friend_sync = parse_friend_sync(data)
        self.integrations = parse_integrations(data)
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
            data['id'] = str(self.id)
        
        put_friend_sync_into(self.friend_sync, data, defaults)
        put_integrations_into(self.integrations, data, defaults, include_internals = include_internals)
        put_name_into(self.name, data, defaults)
        put_revoked_into(self.revoked, data, defaults)
        put_show_activity_into(self.show_activity, data, defaults)
        put_two_way_link_into(self.two_way_link, data, defaults)
        put_type_into(self.type, data, defaults)
        put_verified_into(self.verified, data, defaults)
        put_visibility_into(self.visibility, data, defaults)
        
        return data
    
    
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        """
        Sets the connection's attributes from the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `Any`) items
            The keyword parameters to set the connection's attributes from.
        
        Raises
        ------
        TypeError
            A field of invalid type.
        ValueError
            A field of invalid value.
        """
        # id
        # Ignore, internal
        
        # friend_sync
        try:
            friend_sync = keyword_parameters.pop('friend_sync')
        except KeyError:
            pass
        else:
            self.friend_sync = validate_friend_sync(friend_sync)
        
        # integrations
        try:
            integrations = keyword_parameters.pop('integrations')
        except KeyError:
            pass
        else:
            self.integrations = validate_integrations(integrations)
        
        # name
        try:
            name = keyword_parameters.pop('name')
        except KeyError:
            pass
        else:
            self.name = validate_name(name)
        
        # revoked
        try:
            revoked = keyword_parameters.pop('revoked')
        except KeyError:
            pass
        else:
            self.revoked = validate_revoked(revoked)
        
        # show_activity
        try:
            show_activity = keyword_parameters.pop('show_activity')
        except KeyError:
            pass
        else:
            self.show_activity = validate_show_activity(show_activity)
        
        # two_way_link
        try:
            two_way_link = keyword_parameters.pop('two_way_link')
        except KeyError:
            pass
        else:
            self.two_way_link = validate_two_way_link(two_way_link)
        
        # type
        try:
            type_ = keyword_parameters.pop('type_')
        except KeyError:
            pass
        else:
            self.type = validate_type(type_)
        
        # verified
        try:
            verified = keyword_parameters.pop('verified')
        except KeyError:
            pass
        else:
            self.verified = validate_verified(verified)
        
        # visibility
        try:
            visibility = keyword_parameters.pop('visibility')
        except KeyError:
            pass
        else:
            self.visibility = validate_visibility(visibility)
    
    
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
