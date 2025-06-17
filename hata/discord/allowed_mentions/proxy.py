__all__ = ('AllowedMentionProxy',)

from scarletio import RichAttributeErrorBaseType, export

from ..role import Role, create_partial_role_from_id
from ..user import UserBase, create_partial_user_from_id

from .constants import STATE_ALLOW_REPLIED_USER_FALSE, STATE_ALLOW_REPLIED_USER_NONE, STATE_ALLOW_REPLIED_USER_TRUE

from .helpers import (
    _nullable_list_difference, _nullable_list_intersection, _nullable_list_symmetric_difference, _nullable_list_union
)
from .utils import is_allowed_mentions_valid


@export
class AllowedMentionProxy(RichAttributeErrorBaseType):
    """
    Proxy class to interact with allowed mentions.
    
    Attributes
    ----------
    _allow_everyone : `int`
        Whether everyone mention is enabled.
    _allow_replied_user : `int`
        Whether replied user can be mentioned.
    _allow_roles : `int`
        Whether all role is enabled.
    _allow_users : `int`
        Whether all user is enabled.
    _allowed_role_ids : `None | list<int>`
        The enabled roles by the proxy.
    _allowed_user_ids : `None | list<int>
        The enabled users by the proxy.
    """
    __slots__ = (
        '_allow_everyone', '_allow_replied_user', '_allow_roles', '_allow_users', '_allowed_role_ids', '_allowed_user_ids'
    )
    
    def __new__(cls, *allowed_mentions):
        """
        Parses allowed mentions
        
        Parameters
        ----------
        *allowed_mentions : `str`, ``UserBase``, ``Role``
            Which user or role can the message ping (or everyone).
        
        Raises
        ------
        TypeError
            If `allowed_mentions` contains an element of invalid type.
        ValueError
            If `allowed_mentions` contains en element of correct type, but an invalid value.
        """
        allow_users = 0
        allow_roles = 0
        allow_everyone = 0
        allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
        allowed_role_ids = None
        allowed_user_ids = None
        
        if allowed_mentions:
            for element in allowed_mentions:
                if isinstance(element, str):
                    if element == '!replied_user':
                        allow_replied_user = STATE_ALLOW_REPLIED_USER_FALSE
                        continue
                    
                    if element == 'replied_user':
                        allow_replied_user = STATE_ALLOW_REPLIED_USER_TRUE
                        continue
                    
                    if element == 'everyone':
                        allow_everyone = 1
                        continue
                    
                    if element == 'users':
                        allow_users = 1
                        continue
                    
                    if element == 'roles':
                        allow_roles = 1
                        continue
                    
                    raise ValueError(
                        f'`allowed_mentions` contains a not valid `str` element: `{element!r}`. `str` '
                        f'elements can be any of: (\'everyone\', \'users\', \'roles\', \'replied_user\', '
                        f'\'!replied_user\').'
                    )
                
                if isinstance(element, UserBase):
                    if allowed_user_ids is None:
                        allowed_user_ids = []
                    
                    allowed_user_ids.append(element.id)
                    continue
                
                if isinstance(element, Role):
                    if allowed_role_ids is None:
                        allowed_role_ids = []
                    
                    allowed_role_ids.append(element.id)
                    continue
                
                raise TypeError(
                    f'`allowed_mentions` can contain `str`, `{Role.__name__}`, `{UserBase.__name__}` elements, got '
                    f' {type(element).__name__}; {element!r}; allowed_mentions = {allowed_mentions!r}.'
                )
            
            if allow_users:
                allowed_user_ids = None
            
            if allow_roles:
                allowed_role_ids = None
        
            
        self = object.__new__(cls)
        self._allow_users = allow_users
        self._allow_roles = allow_roles
        self._allow_everyone = allow_everyone
        self._allow_replied_user = allow_replied_user
        self._allowed_role_ids = allowed_role_ids
        self._allowed_user_ids = allowed_user_ids
        return self
    
    
    @classmethod
    def _create_from_various(cls, other):
        """
        Creates an allowed mention proxy instance from other object.
        
        Parameters
        ----------
        other : `instance<cls> | str, (list | set | tuple)<str | UserBase, Role>`
            The other instance to create allowed mention proxy from.
        
        Returns
        -------
        self : `instance<cls>`
        """
        if isinstance(other, cls):
            return other
        
        if isinstance(other, (list, set, tuple)):
            return cls(*other)
        
        return cls(other)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new allowed mention proxy from the given data.
        
        Parameters
        ----------
        data : `None | dict<str, object>`items
            Allowed mention data.
        
        Returns
        -------
        self : `instance<cls>`
            The created allowed mention proxy.
        """
        if (data is None) or (not data):
            allow_users = 0
            allow_roles = 0
            allow_everyone = 0
            allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
            allowed_role_ids = None
            allowed_user_ids = None
            
        else:
            try:
                allow_replied_user_raw = data['replied_user']
            except KeyError:
                allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
            else:
                if allow_replied_user_raw:
                    allow_replied_user = STATE_ALLOW_REPLIED_USER_TRUE
                else:
                    allow_replied_user = STATE_ALLOW_REPLIED_USER_FALSE
            
            allowed_role_ids_raw = data.get('roles', None)
            if (allowed_role_ids_raw is None) or (not allowed_role_ids_raw):
                allowed_role_ids = None
            else:
                allowed_role_ids = []
                for role_id in allowed_role_ids_raw:
                    role_id = int(role_id)
                    allowed_role_ids.append(role_id)
            
            allowed_user_ids_raw = data.get('users', None)
            if (allowed_user_ids_raw is None) or (not allowed_user_ids_raw):
                allowed_user_ids = None
            else:
                allowed_user_ids = []
                for user_id in allowed_user_ids_raw:
                    user_id = int(user_id)
                    allowed_user_ids.append(user_id)
            
            try:
                parse_all_of = data['parse']
            except KeyError:
                allow_users = 0
                allow_roles = 0
                allow_everyone = 0
            else:
                if 'everyone' in parse_all_of:
                    allow_everyone = 1
                else:
                    allow_everyone = 0
                
                if 'roles' in parse_all_of:
                    allow_roles = 1
                else:
                    allow_roles = 0
                
                if 'users' in parse_all_of:
                    allow_users = 1
                else:
                    allow_users = 0
        
        self = object.__new__(cls)
        self._allow_users = allow_users
        self._allow_roles = allow_roles
        self._allow_everyone = allow_everyone
        self._allow_replied_user = allow_replied_user
        self._allowed_role_ids = allowed_role_ids
        self._allowed_user_ids = allowed_user_ids
        return self
    
    
    def to_data(self):
        """
        Converts the allowed mention proxy to json serializable object.
        
        Returns
        -------
        data : `dict<str, object> items
        """
        data = {}
        parse_all_of = None
        
        allow_replied_user = self._allow_replied_user
        if allow_replied_user != STATE_ALLOW_REPLIED_USER_NONE:
            data['replied_user'] = (allow_replied_user == STATE_ALLOW_REPLIED_USER_TRUE)
        
        if self._allow_everyone:
            if parse_all_of is None:
                parse_all_of = []
                data['parse'] = parse_all_of
            
            parse_all_of.append('everyone')
        
        if self._allow_users:
            if parse_all_of is None:
                parse_all_of = []
                data['parse'] = parse_all_of
            
            parse_all_of.append('users')
        else:
            allowed_user_ids = self._allowed_user_ids
            if (allowed_user_ids is not None):
                data['users'] = [str(user_id) for user_id in allowed_user_ids]
        
        if self._allow_roles:
            if parse_all_of is None:
                parse_all_of = []
                data['parse'] = parse_all_of
            
            parse_all_of.append('roles')
        else:
            allowed_role_ids = self._allowed_role_ids
            if (allowed_role_ids is not None):
                data['roles'] = [str(role_id) for role_id in allowed_role_ids]
        
        # Set nothing to parse if we did not set anything.
        if not data:
            data['parse'] = []
        
        return data
    
    
    def __repr__(self):
        """Returns the allowed mention proxy's representation."""
        repr_parts = ['<', type(self).__name__]
        
        field_added = False
        
        # allow_everyone
        allow_everyone = self._allow_everyone
        if allow_everyone:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' allow_everyone = ')
            repr_parts.append(repr(True if allow_everyone else False))
        
        # allow_replied_user
        allow_replied_user = self._allow_replied_user
        if allow_replied_user != STATE_ALLOW_REPLIED_USER_NONE:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' allow_replied_user = ')
            repr_parts.append(repr((allow_replied_user == STATE_ALLOW_REPLIED_USER_TRUE)))
        
        # allow_roles
        allow_roles = self._allow_roles
        if allow_roles:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' allow_roles = ')
            repr_parts.append(repr(True if allow_roles else allow_roles))
        
        # allow_users
        allow_users = self._allow_users
        if allow_users:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' allow_users = ')
            repr_parts.append(repr(True if allow_users else False))
        
        # allowed_role_ids
        allowed_role_ids = self._allowed_role_ids
        if (allowed_role_ids is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' allowed_role_ids = [')
            
            limit = len(allowed_role_ids)
            index = 0
            
            while True:
                role_id = allowed_role_ids[index]
                repr_parts.append(repr(role_id))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        # allowed_user_ids
        allowed_user_ids = self._allowed_user_ids
        if (allowed_user_ids is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' allowed_user_ids = [')
            
            limit = len(allowed_user_ids)
            index = 0
            
            while True:
                user_id = allowed_user_ids[index]
                repr_parts.append(repr(user_id))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def copy(self):
        """
        Copies the allowed mention proxy.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        allowed_role_ids = self._allowed_role_ids
        if (allowed_role_ids is not None):
            allowed_role_ids = allowed_role_ids.copy()
        
        allowed_user_ids = self._allowed_user_ids
        if (allowed_user_ids is not None):
            allowed_user_ids = allowed_user_ids.copy()
        
        new = object.__new__(type(self))
        new._allow_everyone = self._allow_everyone
        new._allow_replied_user = self._allow_replied_user
        new._allow_roles = self._allow_roles
        new._allow_users = self._allow_users
        new._allowed_role_ids = allowed_role_ids
        new._allowed_user_ids = allowed_user_ids
        return new
    
    
    def __eq__(self, other):
        """Returns whether the two allowed mention proxies are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self._allow_users != other._allow_users:
            return False
        
        if self._allow_roles != other._allow_roles:
            return False
        
        if self._allow_everyone != other._allow_everyone:
            return False
        
        if self._allow_replied_user != other._allow_replied_user:
            return False
        
        if self._allowed_role_ids != other._allowed_role_ids:
            return False
        
        if self._allowed_user_ids != other._allowed_user_ids:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the allowed mention proxy's hash value."""
        hash_value = 0
        hash_value ^= self._allow_users << 3
        hash_value ^= self._allow_roles << 6
        hash_value ^= self._allow_everyone << 9
        hash_value ^= self._allow_replied_user << 12
        
        allowed_role_ids = self._allowed_role_ids
        if (allowed_role_ids is not None):
            hash_value ^= len(allowed_role_ids) << 16
            for role_id in allowed_role_ids:
                hash_value ^= role_id

        allowed_user_ids = self._allowed_user_ids
        if (allowed_user_ids is not None):
            hash_value ^= len(allowed_user_ids) << 24
            for user_id in allowed_user_ids:
                hash_value ^= user_id
        
        return hash_value
    
    
    def __and__(self, other):
        """Returns the intersection of the two allowed mention proxy."""
        if not is_allowed_mentions_valid(other):
            return NotImplemented
        
        other = self._create_from_various(other)
        
        
        allow_roles = self._allow_roles & other._allow_roles
        
        allow_users = self._allow_users & other._allow_users
        
        allow_everyone = self._allow_everyone & other._allow_everyone
        
        allow_replied_user = self._allow_replied_user
        if allow_replied_user != other._allow_replied_user:
            allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
        
        if allow_roles:
            allowed_role_ids = None
        
        elif self._allow_roles:
            allowed_role_ids = other._allowed_role_ids
            if (allowed_role_ids is not None):
                allowed_role_ids = allowed_role_ids.copy()
        
        elif other._allow_roles:
            allowed_role_ids = self._allowed_role_ids
            if (allowed_role_ids is not None):
                allowed_role_ids = allowed_role_ids.copy()
        else:
            allowed_role_ids = _nullable_list_intersection(self._allowed_role_ids, other._allowed_role_ids)
        
        if allow_users:
            allowed_user_ids = None
        
        elif self._allow_users:
            allowed_user_ids = other._allowed_user_ids
            if (allowed_user_ids is not None):
                allowed_user_ids = allowed_user_ids.copy()
        
        elif other._allow_users:
            allowed_user_ids = self._allowed_user_ids
            if (allowed_user_ids is not None):
                allowed_user_ids = allowed_user_ids.copy()
        else:
            allowed_user_ids = _nullable_list_intersection(self._allowed_user_ids, other._allowed_user_ids)
        
        new = object.__new__(type(self))
        new._allow_everyone = allow_everyone
        new._allow_replied_user = allow_replied_user
        new._allow_roles = allow_roles
        new._allow_users = allow_users
        new._allowed_role_ids = allowed_role_ids
        new._allowed_user_ids = allowed_user_ids
        
        return new
    
    
    __rand__ = __and__
    
    
    def __xor__(self, other):
        """Returns the symmetric difference of the two allowed mention proxy."""
        if not is_allowed_mentions_valid(other):
            return NotImplemented
        
        other = self._create_from_various(other)
        
        
        allow_roles = self._allow_roles ^ other._allow_roles
        
        allow_users = self._allow_users ^ other._allow_users
        
        allow_everyone = self._allow_everyone ^ other._allow_everyone
        
        self_allow_replied_user = self._allow_replied_user
        other_allow_replied_user = other._allow_replied_user
        if self_allow_replied_user == STATE_ALLOW_REPLIED_USER_NONE:
            allow_replied_user = other_allow_replied_user
        elif other_allow_replied_user == STATE_ALLOW_REPLIED_USER_NONE:
            allow_replied_user = self_allow_replied_user
        else:
            allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
        
        if allow_roles:
            allowed_role_ids = None
        else:
            allowed_role_ids = _nullable_list_symmetric_difference(self._allowed_role_ids, other._allowed_role_ids)
        
        if allow_users:
            allowed_user_ids = None
        else:
            allowed_user_ids = _nullable_list_symmetric_difference(self._allowed_user_ids, other._allowed_user_ids)
        
        new = object.__new__(type(self))
        new._allow_everyone = allow_everyone
        new._allow_replied_user = allow_replied_user
        new._allow_roles = allow_roles
        new._allow_users = allow_users
        new._allowed_role_ids = allowed_role_ids
        new._allowed_user_ids = allowed_user_ids
        
        return new
    
    
    __rxor__ = __xor__
    
    
    def __or__(self, other):
        """Returns the union of the two allowed mention proxy."""
        if not is_allowed_mentions_valid(other):
            return NotImplemented
        
        other = self._create_from_various(other)
        
        allow_roles = self._allow_roles | other._allow_roles
        
        allow_users = self._allow_users | other._allow_users
        
        allow_everyone = self._allow_everyone | other._allow_everyone
        
        self_allow_replied_user = self._allow_replied_user
        other_allow_replied_user = other._allow_replied_user
        if self_allow_replied_user == STATE_ALLOW_REPLIED_USER_NONE:
            allow_replied_user = other_allow_replied_user
        elif other_allow_replied_user == STATE_ALLOW_REPLIED_USER_NONE:
            allow_replied_user = self_allow_replied_user
        elif self_allow_replied_user == other_allow_replied_user:
            allow_replied_user = self_allow_replied_user
        else:
            allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
        
        if allow_roles:
            allowed_role_ids = None
        else:
            allowed_role_ids = _nullable_list_union(self._allowed_role_ids, other._allowed_role_ids)
        
        if allow_users:
            allowed_user_ids = None
        else:
            allowed_user_ids = _nullable_list_union(self._allowed_user_ids, other._allowed_user_ids)
        
        
        new = object.__new__(type(self))
        new._allow_everyone = allow_everyone
        new._allow_replied_user = allow_replied_user
        new._allow_roles = allow_roles
        new._allow_users = allow_users
        new._allowed_role_ids = allowed_role_ids
        new._allowed_user_ids = allowed_user_ids
        
        return new
    
    
    __ror__ = __or__
    __add__ = __or__
    __radd__ = __or__
    
    
    @classmethod
    def _subtract(cls, self, other):
        """
        Returns an allowed mentions proxy, without elements found in other.
        
        This is a classmethod.
        
        Parameters
        ----------
        self : `instance<type<self>>`
            The allowed mention proxy to subtract the other from.
        other : `instance<type<self>>`
            The allowed mention proxy to subtract.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        if other._allow_roles:
            allow_roles = 0
        else:
            allow_roles = self._allow_roles
        
        if other._allow_users:
            allow_users = 0
        else:
            allow_users = self._allow_users
        
        if other._allow_everyone:
            allow_everyone = 0
        else:
            allow_everyone = self._allow_everyone
        
        self_allow_replied_user = self._allow_replied_user
        other_allow_replied_user = other._allow_replied_user
        if self_allow_replied_user == STATE_ALLOW_REPLIED_USER_NONE:
            allow_replied_user = self_allow_replied_user
        elif other_allow_replied_user == STATE_ALLOW_REPLIED_USER_NONE:
            allow_replied_user = self_allow_replied_user
        elif self_allow_replied_user == other_allow_replied_user:
            allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
        else:
            allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
        
        if allow_roles or other._allow_roles:
            allowed_role_ids = None
        else:
            allowed_role_ids = _nullable_list_difference(self._allowed_role_ids, other._allowed_role_ids)
        
        if allow_users or other._allow_users:
            allowed_user_ids = None
        else:
            allowed_user_ids = _nullable_list_difference(self._allowed_user_ids, other._allowed_user_ids)
        
        new = object.__new__(type(self))
        new._allow_roles = allow_roles
        new._allow_users = allow_users
        new._allow_everyone = allow_everyone
        new._allow_replied_user = allow_replied_user
        new._allowed_role_ids = allowed_role_ids
        new._allowed_user_ids = allowed_user_ids
        
        return new
    
    
    def __sub__(self, other):
        """Returns an allowed mentions proxy, without elements found in other."""
        if not is_allowed_mentions_valid(other):
            return NotImplemented
        
        other = self._create_from_various(other)
        return self._subtract(self, other)
    
    
    def __rsub__(self, other):
        """Returns an allowed mentions proxy, without elements found in self."""
        if not is_allowed_mentions_valid(other):
            return NotImplemented
        
        other = self._create_from_various(other)
        return self._subtract(other, self)
    
    
    def __iter__(self):
        """
        Iterates back the values which with a same allowed mention proxy can be created.
        
        This method is an iterable generator.
        
        Yields
        ------
        allowed_mentions : `str`, ``UserBase``, ``Role``
            Which user or role can the message ping (or everyone).
        """
        
        if self._allow_everyone:
            yield 'everyone'
        
        allow_replied_user = self._allow_replied_user
        if allow_replied_user == STATE_ALLOW_REPLIED_USER_TRUE:
            yield 'replied_user'
        elif allow_replied_user == STATE_ALLOW_REPLIED_USER_FALSE:
            yield '!replied_user'
        
        if self._allow_roles:
            yield 'roles'
        
        if self._allow_users:
            yield 'users'
        
        
        allowed_role_ids = self._allowed_role_ids
        if (allowed_role_ids is not None):
            for role_id in allowed_role_ids:
                yield create_partial_role_from_id(role_id)
        
        allowed_user_ids = self._allowed_user_ids
        if (allowed_user_ids is not None):
            for user_id in allowed_user_ids:
                yield create_partial_user_from_id(user_id)
    
    
    def update(self, other):
        """
        Updates the allowed mentions with the given value.
        
        Parameters
        ----------
        other : `str`, ``UserBase``, ``Role``, `instance<type<self>>` or (`list`, `tuple`, `set`) of \
                (`str`, ``UserBase``, ``Role``)
            Which user or role can the message ping (or everyone).
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            If `other` contains an element of invalid type.
        ValueError
            If `other` contains en element of correct type, but an invalid value.
        """
        other = self._create_from_various(other)
        
        allow_replied_user = other._allow_replied_user
        if allow_replied_user != STATE_ALLOW_REPLIED_USER_NONE:
            self._allow_replied_user = allow_replied_user
        
        allow_everyone = other._allow_everyone
        if allow_everyone:
            self._allow_everyone = allow_everyone
        
        allow_roles = other._allow_roles
        if allow_roles:
            self._allow_roles = allow_roles
            self._allowed_role_ids = None
        else:
            if not self._allow_roles:
                self._allowed_role_ids = _nullable_list_union(self._allowed_role_ids, other._allowed_role_ids)
        
        
        allow_users = other._allow_users
        if allow_users:
            self._allow_users = allow_users
            self._allowed_user_ids = None
        else:
            if not self._allow_users:
                self._allowed_user_ids = _nullable_list_union(self._allowed_user_ids, other._allowed_user_ids)
    
    
    @property
    def allow_roles(self):
        """
        A get-set-del property to enable or disable role mentions.
        
        Accepts and returns `bool`-s.
        """
        if self._allow_roles:
            allow_roles_output = True
        else:
            allow_roles_output = False
        
        return allow_roles_output
    
    
    @allow_roles.setter
    def allow_roles(self, allow_roles_input):
        if not isinstance(allow_roles_input, bool):
            raise TypeError(
                f'`allow_roles` can be `bool`, got '
                f'{type(allow_roles_input).__name__}; {allow_roles_input!r}.'
            )
        
        if allow_roles_input:
            allow_roles = 1
            self._allowed_role_ids = None
        else:
            allow_roles = 0
        
        self._allow_roles = allow_roles
    
    
    @allow_roles.deleter
    def allow_roles(self):
        self._allow_roles = 0
    
    
    @property
    def allow_users(self):
        """
        A get-set-del property to enable or disable user mentions.
        
        Accepts and returns `bool`-s.
        """
        if self._allow_users:
            allow_users_output = True
        else:
            allow_users_output = False
        
        return allow_users_output
    
    
    @allow_users.setter
    def allow_users(self, allow_users_input):
        if not isinstance(allow_users_input, bool):
            raise TypeError(
                f'`allow_users` can be `bool`, got '
                f'{type(allow_users_input).__name__}; {allow_users_input!r}.'
            )
        
        if allow_users_input:
            allow_users = 1
            self._allowed_user_ids = None
        else:
            allow_users = 0
        
        self._allow_users = allow_users
    
    
    @allow_users.deleter
    def allow_users(self):
        self._allow_users = 0
    
    
    @property
    def allow_everyone(self):
        """
        A get-set-del property to enable or disable everyone mentions.
        
        Accepts and returns `bool`-s.
        """
        if self._allow_everyone:
            allow_everyone_output = True
        else:
            allow_everyone_output = False
        
        return allow_everyone_output
    
    
    @allow_everyone.setter
    def allow_everyone(self, allow_everyone_input):
        if not isinstance(allow_everyone_input, bool):
            raise TypeError(
                f'`allow_everyone` can be `bool`, got '
                f'{type(allow_everyone_input).__name__}; {allow_everyone_input!r}.'
            )
        
        if allow_everyone_input:
            allow_everyone = 1
        else:
            allow_everyone = 0
        
        self._allow_everyone = allow_everyone
    
    
    @allow_everyone.deleter
    def allow_everyone(self):
        self._allow_everyone = 0
    
    
    @property
    def allow_replied_user(self):
        """
        A get-set-del property to enable or disable replied user mention.
        
        Accepts and returns `None` and `bool`-s.
        """
        allow_replied_user = self._allow_replied_user
        if allow_replied_user == STATE_ALLOW_REPLIED_USER_NONE:
            allow_replied_user_output = None
        elif allow_replied_user == STATE_ALLOW_REPLIED_USER_TRUE:
            allow_replied_user_output = True
        else:
            allow_replied_user_output = False
        
        return allow_replied_user_output
    
    
    @allow_replied_user.setter
    def allow_replied_user(self, allow_replied_user_input):
        if (allow_replied_user_input is not None) and (not isinstance(allow_replied_user_input, bool)):
            raise TypeError(
                f'`allow_replied_user` can be `None | int`, got '
                f'{type(allow_replied_user_input).__name__}; {allow_replied_user_input!r}.'
            )
        
        if allow_replied_user_input is None:
            allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
        elif allow_replied_user_input:
            allow_replied_user = STATE_ALLOW_REPLIED_USER_TRUE
        else:
            allow_replied_user = STATE_ALLOW_REPLIED_USER_FALSE
        
        self._allow_replied_user = allow_replied_user
    
    
    @allow_replied_user.deleter
    def allow_replied_user(self):
        self._allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
    
    
    @property
    def allowed_roles(self):
        """
        A get-set-del property to enable or disable specific role mentions.
        
        Accepts and returns ``None | (list | set | tuple)<Role>``
        """
        allowed_role_ids = self._allowed_role_ids
        if allowed_role_ids is not None:
            return [create_partial_role_from_id(role_id) for role_id in allowed_role_ids]
    
    
    @allowed_roles.setter
    def allowed_roles(self, allowed_roles):
        if self._allow_roles:
            return
        
        if allowed_roles is None:
            allowed_role_ids = None
        
        elif isinstance(allowed_roles, Role):
            allowed_role_ids = [allowed_roles.id]
        
        elif isinstance(allowed_roles, (list, set, tuple)):
            allowed_role_ids = None
            
            for role in allowed_roles:
                if not isinstance(role, Role):
                    raise TypeError(
                        f'`allowed_roles` can contain `{Role.__name__}` elements, got '
                        f'{type(role).__name__}; {role!r}; allowed_role_ids_input = {allowed_roles!r}.'
                    )
                
                if allowed_role_ids is None:
                    allowed_role_ids = []
                
                allowed_role_ids.append(role.id)
        else:
            raise TypeError(
                f'`allowed_roles` can be `None`, `{Role.__name__}`, `list`, `tuple`, `set` of {Role.__name__}`'
                f', got {type(allowed_roles).__name__}; {allowed_roles!r}.'
            )
        
        self._allowed_role_ids = allowed_role_ids
    
    
    @allowed_roles.deleter
    def allowed_roles(self):
        self._allowed_role_ids = None
    

    @property
    def allowed_users(self):
        """
        A get-set-del property to enable or disable specific user mentions.
        
        Accepts and returns `None` or a `list`, `set` or `tuple` of ``UserBase``-s.
        """
        allowed_user_ids = self._allowed_user_ids
        if allowed_user_ids is not None:
            return [create_partial_user_from_id(user_id) for user_id in allowed_user_ids]
    
    
    @allowed_users.setter
    def allowed_users(self, allowed_users):
        if self._allow_users:
            return
        
        if allowed_users is None:
            allowed_user_ids = None
        
        elif isinstance(allowed_users, UserBase):
            allowed_user_ids = [allowed_users.id]
        
        elif isinstance(allowed_users, (list, set, tuple)):
            allowed_user_ids = None
            
            for user in allowed_users:
                if not isinstance(user, UserBase):
                    raise TypeError(
                        f'`allowed_users` can contain `{UserBase.__name__}` elements, got '
                        f'{type(user).__name__}; {user!r}; allowed_user_ids_input = {allowed_users!r}.'
                    )
                
                if allowed_user_ids is None:
                    allowed_user_ids = []
                
                allowed_user_ids.append(user.id)
        else:
            raise TypeError(
                f'`allowed_users` can be `None`, `{UserBase.__name__}`, `list`, `tuple`, `set` of '
                f'`{UserBase.__name__}`, got {type(allowed_users).__name__}; {allowed_users!r}.'
            )
        
        self._allowed_user_ids = allowed_user_ids
    
    
    @allowed_users.deleter
    def allowed_users(self):
        self._allowed_user_ids = None
