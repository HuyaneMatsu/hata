__all__ = ('AllowedMentionProxy', 'parse_allowed_mentions')

from .role import Role, create_partial_role_from_id
from .user import UserBase, create_partial_user_from_id



STATE_ALLOW_REPLIED_USER_FALSE = -1
STATE_ALLOW_REPLIED_USER_NONE = 0
STATE_ALLOW_REPLIED_USER_TRUE = 1


def parse_allowed_mentions(allowed_mentions):
    """
    If `allowed_mentions` is passed as `None`, then returns a `dict`, what will cause all mentions to be disabled.
    
    If passed as an `iterable`, then it's elements will be checked. They can be either type `str`
    (any value from `('everyone', 'users', 'roles')`), ``UserBase``, ``Role``-s.
    
    Passing `everyone` will allow the message to mention `@everyone` (permissions can overwrite this behaviour).
    
    Passing `'users'` will allow the message to mention all the users, meanwhile passing ``UserBase``-s.
    allow to mentioned the respective users. Using `users` and ``UserBase``-s. is mutually exclusive,
    and the wrapper will register only `users` to avoid getting ``DiscordException``.
    
    `'roles'` and ``Role``-s. follow the same rules as `'users'` and the ``UserBase``-s.
    
    By passing `'!replied_user'` you can disable mentioning the replied user, or by passing`'replied_user'` you can
    re-enable mentioning the replied user.
    
    Parameters
    ----------
    allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, ``AllowedMentionProxy``, (`list`, `tuple`, `set`) of \
            (`str`, ``UserBase``, ``Role`` )
        Which user or role can the message ping (or everyone).
    
    Returns
    -------
    allowed_mentions : `dict` of (`str`, `object`) items
    
    Raises
    ------
    TypeError
        If `allowed_mentions` contains an element of invalid type.
    ValueError
        If `allowed_mentions` contains en element of correct type, but an invalid value.
    """
    if (allowed_mentions is None):
        return {'parse': []}
    
    if isinstance(allowed_mentions, AllowedMentionProxy):
        return allowed_mentions.to_data()
    
    if isinstance(allowed_mentions, list):
        if (not allowed_mentions):
            return {'parse': []}
    elif isinstance(allowed_mentions, (set, tuple)):
        if (not allowed_mentions):
            return {'parse': []}
        
        allowed_mentions = list(allowed_mentions)
    
    else:
        allowed_mentions = [allowed_mentions]
    
    allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
    allow_everyone = 0
    allow_users = 0
    allow_roles = 0
    
    allowed_users = None
    allowed_roles = None
    
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
            if allowed_users is None:
                allowed_users = []
            
            allowed_users.append(element.id)
            continue
        
        if isinstance(element, Role):
            if allowed_roles is None:
                allowed_roles = []
            
            allowed_roles.append(element.id)
            continue
        
        raise TypeError(
            f'`allowed_mentions` can contain `str`, `{Role.__name__}`, `{UserBase.__name__}` elements, got '
            f' {element.__class__.__name__}; {element!r}; allowed_mentions={allowed_mentions!r}.'
        )
    
    
    result = {}
    parse_all_of = None
    
    if allow_replied_user != STATE_ALLOW_REPLIED_USER_NONE:
        result['replied_user'] = (allow_replied_user == STATE_ALLOW_REPLIED_USER_TRUE)
    
    if allow_everyone:
        if parse_all_of is None:
            parse_all_of = []
            result['parse'] = parse_all_of
        
        parse_all_of.append('everyone')
    
    if allow_users:
        if parse_all_of is None:
            parse_all_of = []
            result['parse'] = parse_all_of
        
        parse_all_of.append('users')
    else:
        if (allowed_users is not None):
            result['users'] = allowed_users
    
    if allow_roles:
        if parse_all_of is None:
            parse_all_of = []
            result['parse'] = parse_all_of
        
        parse_all_of.append('roles')
    else:
        if (allowed_roles is not None):
            result['roles'] = allowed_roles
    
    return result


def _nullable_list_intersection(list_1, list_2):
    """
    Returns the intersection of 2 nullable lists.
    
    Parameters
    ----------
    list_1 : `None` or `list` of ``DiscordEntity``
        First list.
    list_2 : `None` or `list` of ``DiscordEntity``
        First list.
    
    Returns
    -------
    intersection : `None` or `list` of ``DiscordEntity``
        A list with the two list's intersection.
    """
    if list_1 is None:
        return None
    
    if list_2 is None:
        return None
    
    intersection = set(list_1) & set(list_2)
    if not intersection:
        return None
    
    return list(intersection)


def _nullable_list_symmetric_difference(list_1, list_2):
    """
    Returns the symmetric difference of 2 nullable lists.
    
    Parameters
    ----------
    list_1 : `None` or `list` of ``DiscordEntity``
        First list.
    list_2 : `None` or `list` of ``DiscordEntity``
        First list.
    
    Returns
    -------
    symmetric_difference : `None` or `list` of ``DiscordEntity``
        A list with the two list's symmetric difference.
    """
    if list_1 is None:
        if list_2 is None:
            return None
        
        else:
            return list_2.copy()
    
    else:
        if list_2 is None:
            return list_1.copy()
    
    symmetric_difference = set(list_1) ^ set(list_2)
    if not symmetric_difference:
        return None
    
    return list(symmetric_difference)


def _nullable_list_union(list_1, list_2):
    """
    Returns the union of 2 nullable lists.
    
    Parameters
    ----------
    list_1 : `None` or `list` of ``DiscordEntity``
        First list.
    list_2 : `None` or `list` of ``DiscordEntity``
        First list.
    
    Returns
    -------
    union : `None` or `list` of ``DiscordEntity``
        A list with the two list's union.
    """
    if list_1 is None:
        if list_2 is None:
            return None
        
        else:
            return list_2.copy()
    
    else:
        if list_2 is None:
            return list_1.copy()
        
        else:
            return list({*list_1, *list_2})


def _nullable_list_difference(list_1, list_2):
    """
    Returns the a copy of `list_1` without the elements of `list_2`.
    
    Parameters
    ----------
    list_1 : `None` or `list` of ``DiscordEntity``
        First list.
    list_2 : `None` or `list` of ``DiscordEntity``
        First list.
    
    Returns
    -------
    difference : `None` or `list` of ``DiscordEntity``
        A list with the two list's difference.
    """
    if list_1 is None:
        return None
    
    if list_2 is None:
        return list_1.copy()
    
    difference = set(list_1) - set(list_2)
    if not difference:
        return None
    
    return list(difference)


class AllowedMentionProxy:
    """
    Proxy class to interact with allowed mentions.
    
    Attributes
    ----------
    _allow_roles : `int`
        Whether all role is enabled.
    _allow_users : `int`
        Whether all user is enabled.
    _allow_everyone : `int`
        Whether everyone mention is enabled.
    _allow_replied_user : `int`
        Whether replied user can be mentioned.
    _allowed_roles : `None`, `list` of ``Role``
        The enabled roles by the proxy.
    _allowed_users : `None`, `list` of ``UserBase``
        The enabled users by the proxy.
    """
    __slots__ = (
        '_allow_everyone', '_allow_replied_user', '_allow_roles', '_allow_users', '_allowed_roles', '_allowed_users'
    )
    
    def __new__(cls, *allowed_mentions):
        """
        Parses allowed mentions
        
        Parameters
        ----------
        *allowed_mentions : `str`, ``UserBase``, ``Role``, ``AllowedMentionProxy``
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
        allowed_roles = None
        allowed_users = None
        
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
                    if allowed_users is None:
                        allowed_users = []
                    
                    allowed_users.append(element)
                    continue
                
                if isinstance(element, Role):
                    if allowed_roles is None:
                        allowed_roles = []
                    
                    allowed_roles.append(element)
                    continue
                
                raise TypeError(
                    f'`allowed_mentions` can contain `str`, `{Role.__name__}`, `{UserBase.__name__}` elements, got '
                    f' {element.__class__.__name__}; {element!r}; allowed_mentions={allowed_mentions!r}.'
                )
            
            if allow_users:
                allowed_users = None
            
            if allow_roles:
                allowed_roles = None
        
            
        self = object.__new__(cls)
        self._allow_users = allow_users
        self._allow_roles = allow_roles
        self._allow_everyone = allow_everyone
        self._allow_replied_user = allow_replied_user
        self._allowed_roles = allowed_roles
        self._allowed_users = allowed_users
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new allowed mention proxy from the given data.
        
        Parameters
        ----------
        data : `None`, `dict` of (`str`, `object`) items
            Allowed mention data
        
        Returns
        -------
        self : ``AllowedMentionProxy``
            The created allowed mention proxy.
        """
        if (data is None) or (not data):
            allow_users = 0
            allow_roles = 0
            allow_everyone = 0
            allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
            allowed_roles = None
            allowed_users = None
            
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
            
            allowed_roles_raw = data.get('roles', None)
            if (allowed_roles_raw is None) or (not allowed_roles_raw):
                allowed_roles = None
            else:
                allowed_roles = []
                for role_id in allowed_roles:
                    role_id = int(role_id)
                    role = create_partial_role_from_id(role_id)
                    allowed_roles.append(role)
            
            allowed_users_raw = data.get('users', None)
            if (allowed_users_raw is None) or (not allowed_users_raw):
                allowed_users = None
            else:
                allowed_users = []
                for user_id in allowed_users_raw:
                    user_id = int(user_id)
                    user = create_partial_user_from_id(user_id)
                    allowed_users.append(user)
            
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
        self._allowed_roles = allowed_roles
        self._allowed_users = allowed_users
        return self
    
    
    def to_data(self):
        """
        Converts the allowed mention proxy to json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
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
            allowed_users = self._allowed_users
            if (allowed_users is not None):
                data['users'] = [user.id for user in allowed_users]
        
        if self._allow_roles:
            if parse_all_of is None:
                parse_all_of = []
                data['parse'] = parse_all_of
            
            parse_all_of.append('roles')
        else:
            allowed_roles = self._allowed_roles
            if (allowed_roles is not None):
                data['roles'] = [role.id for role in allowed_roles]
        
        return data
    
    def __repr__(self):
        """Returns the allowed mention proxy's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        allow_replied_user = self._allow_replied_user
        if allow_replied_user != STATE_ALLOW_REPLIED_USER_NONE:
            field_added = True
            
            repr_parts.append(' allow_replied_user = ')
            repr_parts.append(repr((allow_replied_user == STATE_ALLOW_REPLIED_USER_TRUE)))
        else:
            field_added = False
        
        allow_everyone = self._allow_everyone
        if allow_everyone:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' allow_everyone=True')
        
        allow_users = self._allow_users
        if allow_users:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' allow_users=True')
        
        
        allow_roles = self._allow_roles
        if allow_roles:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' allow_roles=True')
        
        
        allowed_users = self._allowed_users
        if (allowed_users is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' allowed_users=[')
            
            limit = len(allowed_users)
            index = 0
            
            while True:
                user = allowed_users[index]
                repr_parts.append(repr(user))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        allowed_roles = self._allowed_roles
        if (allowed_roles is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' allowed_roles=[')
            
            limit = len(allowed_roles)
            index = 0
            
            while True:
                role = allowed_roles[index]
                repr_parts.append(repr(role))
                
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
        allowed_roles = self._allowed_roles
        if (allowed_roles is not None):
            allowed_roles = allowed_roles.copy()
        
        allowed_users = self._allowed_users
        if (allowed_users is not None):
            allowed_users = allowed_users.copy()
        
        new = object.__new__(type(self))
        new._allow_users = self._allow_users
        new._allow_roles = self._allow_roles
        new._allow_everyone = self._allow_everyone
        new._allow_replied_user = self._allow_replied_user
        new._allowed_roles = allowed_roles
        new._allowed_users = allowed_users
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
        
        if self._allowed_roles != other._allowed_roles:
            return False
        
        if self._allowed_users != other._allowed_users:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the allowed mention proxy's hash value."""
        hash_value = 0
        hash_value ^= self._allow_users << 3
        hash_value ^= self._allow_roles << 6
        hash_value ^= self._allow_everyone << 9
        hash_value ^= self._allow_replied_user << 12
        
        allowed_roles = self._allowed_roles
        if (allowed_roles is not None):
            hash_value ^= len(allowed_roles) << 16
            for role in allowed_roles:
                hash_value ^= role.id

        allowed_users = self._allowed_users
        if (allowed_users is not None):
            hash_value ^= len(allowed_users) << 24
            for user in allowed_users:
                hash_value ^= user.id
        
        return hash_value
    
    
    def __and__(self, other):
        """Returns the intersection of the two allowed mention proxy."""
        if not isinstance(other, type(self)):
            try:
                other = type(self)().update(other)
            except (ValueError, TypeError):
                return NotImplemented
        
        allow_roles = self._allow_roles & other._allow_roles
        
        allow_users = self._allow_users & other._allow_users
        
        allow_everyone = self._allow_everyone & other._allow_everyone
        
        allow_replied_user = self.allow_replied_user
        if allow_replied_user != other._allow_replied_user:
            allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
        
        if allow_roles:
            allowed_roles = None
        else:
            allowed_roles = _nullable_list_intersection(self._allowed_roles, other._allowed_roles)
        
        if allow_users:
            allowed_users = None
        else:
            allowed_users = _nullable_list_intersection(self._allowed_users, other._allowed_users)
        
        new = type(self)()
        new._allow_roles = allow_roles
        new._allow_users = allow_users
        new._allow_everyone = allow_everyone
        new._allow_replied_user = allow_replied_user
        new._allowed_roles = allowed_roles
        new._allowed_users = allowed_users
        
        return new
    
    __rand__ = __and__
    
    def __xor__(self, other):
        """Returns the symmetric difference of the two allowed mention proxy."""
        if not isinstance(other, type(self)):
            try:
                other = type(self)().update(other)
            except (ValueError, TypeError):
                return NotImplemented
        
        
        allow_roles = self._allow_roles ^ other._allow_roles
        
        allow_users = self._allow_users ^ other._allow_users
        
        allow_everyone = self._allow_everyone ^ other._allow_everyone
        
        self_allow_replied_user = self.allow_replied_user
        other_allow_replied_user = other._allow_replied_user
        if self_allow_replied_user == STATE_ALLOW_REPLIED_USER_NONE:
            allow_replied_user = other_allow_replied_user
        elif other_allow_replied_user == STATE_ALLOW_REPLIED_USER_NONE:
            allow_replied_user = self_allow_replied_user
        else:
            allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
        
        if allow_roles:
            allowed_roles = None
        else:
            allowed_roles = _nullable_list_symmetric_difference(self._allowed_roles, other._allowed_roles)
        
        if allow_users:
            allowed_users = None
        else:
            allowed_users = _nullable_list_symmetric_difference(self._allowed_users, other._allowed_users)
        
        new = type(self)()
        
        new._allow_roles = allow_roles
        new._allow_users = allow_users
        new._allow_everyone = allow_everyone
        new._allow_replied_user = allow_replied_user
        new._allowed_roles = allowed_roles
        new._allowed_users = allowed_users
        
        return new
    
    __rxor__ = __xor__
    
    def __or__(self, other):
        """Returns the union of the two allowed mention proxy."""
        if not isinstance(other, type(self)):
            try:
                other = type(self)().update(other)
            except (ValueError, TypeError):
                return NotImplemented
        
        
        allow_roles = self._allow_roles | other._allow_roles
        
        allow_users = self._allow_users | other._allow_users
        
        allow_everyone = self._allow_everyone | other._allow_everyone
        
        self_allow_replied_user = self.allow_replied_user
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
            allowed_roles = None
        else:
            allowed_roles = _nullable_list_union(self._allowed_roles, other._allowed_roles)
        
        if allow_users:
            allowed_users = None
        else:
            allowed_users = _nullable_list_union(self._allowed_users, other._allowed_users)
            
        new = type(self)()
        
        new._allow_roles = allow_roles
        new._allow_users = allow_users
        new._allow_everyone = allow_everyone
        new._allow_replied_user = allow_replied_user
        new._allowed_roles = allowed_roles
        new._allowed_users = allowed_users
        
        return new
    
    __ror__ = __or__
    __add__ = __or__
    __radd__ = __or__
    
    
    @classmethod
    def _difference(cls, self, other):
        """
        Returns an allowed mentions proxy, without elements found in other.
        
        This is a classmethod.
        
        Parameters
        ----------
        self : ``AllowedMentionProxy``
            The allowed mention proxy to subtract the other from.
        other : ``AllowedMentionProxy``
            The allowed mention proxy to subtract.
        
        Returns
        -------
        new : ``AllowedMentionProxy``
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
            allow_everyone = other._allow_everyone
        
        self_allow_replied_user = self.allow_replied_user
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
            allowed_roles = _nullable_list_difference(self._allowed_roles, other._allowed_roles)
        else:
            allowed_roles = None
        
        if allow_users:
            allowed_users = _nullable_list_difference(self._allowed_users, other._allowed_users)
        else:
            allowed_users = None
        
        new = type(cls)()
        
        new._allow_roles = allow_roles
        new._allow_users = allow_users
        new._allow_everyone = allow_everyone
        new._allow_replied_user = allow_replied_user
        new._allowed_roles = allowed_roles
        new._allowed_users = allowed_users
        
        return new
    
    
    def __sub__(self, other):
        """Returns an allowed mentions proxy, without elements found in other."""
        if not isinstance(other, type(self)):
            try:
                other = type(self)().update(other)
            except (ValueError, TypeError):
                return NotImplemented
        
        return self._difference(self, other)
        
    
    def __rsub__(self, other):
        """Returns an allowed mentions proxy, without elements found in self."""
        if not isinstance(other, type(self)):
            try:
                other = type(self)().update(other)
            except (ValueError, TypeError):
                return NotImplemented
        
        return self._difference(other, self)
    
    
    def __iter__(self):
        """
        Iterates back the values which with a same allowed mention proxy can be created.
        
        This method is an iterable generator.
        
        Yields
        ------
        allowed_mentions : `str`, ``UserBase``, ``Role``
            Which user or role can the message ping (or everyone).
        """
        if self._allow_roles:
            yield 'roles'
        
        if self._allow_users:
            yield 'users'
        
        if self._allow_everyone:
            yield 'everyone'
        
        allow_replied_user = self._allow_replied_user
        if allow_replied_user == STATE_ALLOW_REPLIED_USER_FALSE:
            yield '!replied_user'
        elif allow_replied_user == STATE_ALLOW_REPLIED_USER_TRUE:
            yield 'replied_user'
        
        allowed_roles = self._allowed_roles
        if (allowed_roles is not None):
            yield from allowed_roles
        
        allowed_users = self.allowed_users
        if (allowed_users is not None):
            yield from allowed_users
    
    
    def update(self, other):
        """
        Updates the allowed mentions with the given value.
        
        Parameters
        ----------
        other : `str`, ``UserBase``, ``Role``, ``AllowedMentionProxy`` or (`list`, `tuple`, `set`) of \
                (`str`, ``UserBase``, ``Role``)
            Which user or role can the message ping (or everyone).
        
        Returns
        -------
        self : ``AllowedMentionProxy``
        
        Raises
        ------
        TypeError
            If `other` contains an element of invalid type.
        ValueError
            If `other` contains en element of correct type, but an invalid value.
        """
        if isinstance(other, type(self)):
            pass
        elif isinstance(other, (list, tuple, set)):
            other = type(self)(*other)
        else:
            other = type(self)(other)
        
        
        allow_replied_user = other._allow_replied_user
        if allow_replied_user != STATE_ALLOW_REPLIED_USER_NONE:
            self._allow_replied_user = allow_replied_user
        
        allow_everyone = other._allow_everyone
        if allow_everyone:
            self._allow_everyone = allow_everyone
        
        allow_roles = other._allow_roles
        if allow_roles:
            self._allow_roles = allow_roles
            self._allowed_roles = None
        else:
            if not self._allow_roles:
                self_allowed_roles = self._allowed_roles
                if self_allowed_roles is None:
                    final_allowed_roles = None
                else:
                    final_allowed_roles = self_allowed_roles.copy()
                
                other_allowed_roles = other._allowed_roles
                if (other_allowed_roles is not None):
                    if final_allowed_roles is None:
                        final_allowed_roles = other_allowed_roles.copy()
                    else:
                        final_allowed_roles.extend(other_allowed_roles)
                
                self._allowed_roles = final_allowed_roles
        
        
        allow_users = other._allow_users
        if allow_users:
            self._allow_users = allow_users
            self._allowed_users = None
        else:
            if not self._allow_users:
                self_allowed_users = self._allowed_users
                if self_allowed_users is None:
                    final_allowed_users = None
                else:
                    final_allowed_users = self_allowed_users.copy()
                
                other_allowed_users = other._allowed_users
                if (other_allowed_users is not None):
                    if final_allowed_users is None:
                        final_allowed_users = other_allowed_users.copy()
                    else:
                        final_allowed_users.extend(other_allowed_users)
                
                self._allowed_users = final_allowed_users
    
    
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
        if __debug__:
            if not isinstance(allow_roles_input, bool):
                raise AssertionError(
                    f'`allow_roles_input` can be `bool`, got '
                    f'{allow_roles_input.__class__.__name__}; {allow_roles_input!r}.'
                )
        
        if allow_roles_input:
            allow_roles = 1
            self._allowed_roles = None
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
        if __debug__:
            if not isinstance(allow_users_input, bool):
                raise AssertionError(
                    f'`allow_users_input` can be `bool`, got '
                    f'{allow_users_input.__class__.__name__}; {allow_users_input!r}.'
                )
        
        if allow_users_input:
            allow_users = 1
            self._allowed_users = None
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
        if __debug__:
            if not isinstance(allow_everyone_input, bool):
                raise AssertionError(
                    f'`allow_everyone_input` can be `bool`, got '
                    f'{allow_everyone_input.__class__.__name__}; {allow_everyone_input!r}.'
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
        if __debug__:
            if (allow_replied_user_input is not None) and (not isinstance(allow_replied_user_input, bool)):
                raise AssertionError(
                    f'`allow_replied_user_input` can be `None`, `bool`, got '
                    f'{allow_replied_user_input.__class__.__name__}; {allow_replied_user_input!r}.'
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
        
        Accepts and returns `None` or a `list` of ``Role``-s.
        """
        allowed_roles = self._allowed_roles
        if allowed_roles is None:
            allowed_roles_output = None
        else:
            allowed_roles_output = allowed_roles.copy()
        
        return allowed_roles_output
    
    @allowed_roles.setter
    def allowed_roles(self, allowed_roles_input):
        if self._allow_roles:
            return
        
        # Use goto
        if allowed_roles_input is None:
            allowed_roles = None
        elif isinstance(allowed_roles_input, Role):
            allowed_roles = [allowed_roles_input]
        elif isinstance(allowed_roles_input, (list, set, tuple)):
            allowed_roles = None
            
            for role in allowed_roles_input:
                if not isinstance(role, Role):
                    raise TypeError(
                        f'`allowed_roles_input` can contain `{Role.__name__}` elements, got '
                        f'{role.__class__.__name__}; {role!r}; allowed_roles_input={allowed_roles_input!r}.'
                    )
                
                if allowed_roles is None:
                    allowed_roles = []
                
                allowed_roles.append(role)
        else:
            raise TypeError(
                f'`allowed_roles_input` can be `None`, `{Role.__name__}`, `list`, `tuple`, `set` of {Role.__name__}`'
                f', got {allowed_roles_input.__class__.__name__}; {allowed_roles_input!r}.'
            )
        
        self._allowed_roles = allowed_roles
    
    @allowed_roles.deleter
    def allowed_roles(self):
        self._allowed_roles = None
    

    @property
    def allowed_users(self):
        """
        A get-set-del property to enable or disable specific user mentions.
        
        Accepts and returns `None` or a `list` of ``Role``-s.
        """
        allowed_users = self._allowed_users
        if allowed_users is None:
            allowed_users_output = None
        else:
            allowed_users_output = allowed_users.copy()
        
        return allowed_users_output
    
    @allowed_users.setter
    def allowed_users(self, allowed_users_input):
        if self._allow_users:
            return
        
        # Use goto
        if allowed_users_input is None:
            allowed_users = None
        elif isinstance(allowed_users_input, Role):
            allowed_users = [allowed_users_input]
        elif isinstance(allowed_users_input, (list, set, tuple)):
            allowed_users = None
            
            for user in allowed_users_input:
                if not isinstance(user, Role):
                    raise TypeError(
                        f'`allowed_users_input` can contain `{UserBase.__name__}` elements, got'
                        f'{user.__class__.__name__}; {user!r}; allowed_users_input={allowed_users_input!r}.'
                    )
                
                if allowed_users is None:
                    allowed_users = []
                
                allowed_users.append(user)
        else:
            raise TypeError(
                f'`allowed_users_input` can be `None`, `{UserBase.__name__}`, `list`, `tuple`, `set` of '
                f'`{UserBase.__name__}`, got {allowed_users_input.__class__.__name__}; {allowed_users_input!r}.'
            )
        
        self._allowed_users = allowed_users
    
    @allowed_users.deleter
    def allowed_users(self):
        self._allowed_users = None
