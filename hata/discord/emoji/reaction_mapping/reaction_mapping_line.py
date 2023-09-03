__all__ = ('ReactionMappingLine',)

from scarletio import include
from scarletio.utils.compact import NEEDS_DUMMY_INIT


Client = include('Client')
ClientUserBase = include('ClientUserBase')


def _validate_reaction_mapping_line_initialise_with(reaction_mapping_line_type, initialize_with):
    """
    Validates the `initialize_with` parameter of ``ReactionMappingLine``.
    
    Parameters
    ----------
    reaction_mapping_line_type : `type`
        The type of the reaction mapping line.
    initialize_with : `None`, `iterable` of (`None`, ``ClientUserBase``), `instance<reaction_mapping_line_type>`
        The value ot initialize the line with.
    
    Returns
    -------
    users : `None`, `list` of ``ClientUserBase``
        The built users from the `initialize_with` parameter.
    unknown : `int`
        The amount of unknown users.
    
    Raises
    ------
    TypeError
        - If an element of `initialize_with` is not `None`, ``ClientUserBase``.
    """
    if initialize_with is None:
        built_initialize_with = None, 0
    
    elif type(initialize_with) is reaction_mapping_line_type:
        built_initialize_with = _validate_reaction_mapping_line_initialise_with_same(initialize_with)
    
    elif (getattr(initialize_with, '__iter__', None) is not None):
        built_initialize_with = _validate_reaction_mapping_line_initialise_with_iterable(initialize_with)
    
    else:
        raise TypeError(
            f'`initialize_with` can be `None`, `{reaction_mapping_line_type.__name__}`, '
            f'`iterable` of (`{ClientUserBase.__name__}`, `None`), got '
            f'{initialize_with.__class__.__name__}; {initialize_with!r}.'
        )
    
    return built_initialize_with


def _validate_reaction_mapping_line_initialise_with_same(initialize_with):
    """
    Validates the `initialize_with` parameter of ``ReactionMappingLine`` where it is the same type.
    
    Parameters
    ----------
    initialize_with : ``ReactionMappingLine``
        The value ot initialize the line with.
    
    Returns
    -------
    users : `None`, `list` of ``ClientUserBase``
        The built users from the `initialize_with` parameter.
    unknown : `int`
        The amount of unknown users.
    """
    if set.__len__(initialize_with) == 0:
        users = None
    else:
        users = [*set.__iter__(initialize_with)]
    
    unknown = initialize_with.unknown
    
    return users, unknown


def _validate_reaction_mapping_line_initialise_with_iterable(initialize_with):
    """
    Validates the `initialize_with` parameter of ``ReactionMappingLine`` where it is an iterable.
    
    Parameters
    ----------
    initialize_with : `iterable` of (`None`, ``ClientUserBase``)
        The value ot initialize the line with.
    
    Returns
    -------
    users : `None`, `list` of ``ClientUserBase``
        The built users from the `initialize_with` parameter.
    unknown : `int`
        The amount of unknown users.
    
    Raises
    ------
    TypeError
        - If an element of `initialize_with` is not `None`, ``ClientUserBase``.
    """
    users = None
    unknown = 0
    
    for user in initialize_with:
        if user is None:
            unknown += 1
            continue
        
        if isinstance(user, ClientUserBase):
            if users is None:
                users = []
            
            users.append(user)
            continue
        
        raise TypeError(
            f'`initialize_with` can contain `{ClientUserBase.__name__}` elements, got '
            f'{user.__class__.__name__}; {user!r}; initialize_with={initialize_with!r}.'
        )
    
    return users, unknown


def _validate_reaction_mapping_line_unknown(unknown):
    """
    Validates the `unknown` parameter of ``ReactionMappingLine``.
    
    Parameters
    ----------
    unknown : `None, `int`
        The given `unknown` value to initialize the reaction line with.
    
    Returns
    -------
    validated_unknown : `int`
    
    Raises
    ------
    TypeError
        - If `unknown` is not `int`, `None`.
    ValueError
        - If `unknown` is negative.
    """
    if unknown is None:
        validated_unknown = 0
    
    elif isinstance(unknown, int):
        if (unknown < 0):
            raise ValueError(
                f'`unknown` cannot be negative, got {unknown!r}.'
            )
        
        validated_unknown = unknown
    
    else:
        raise TypeError(
            f'`unknown` can be `None`, `int`, got {unknown.__class__.__name__}; {unknown!r}.'
        )
    
    return validated_unknown


class ReactionMappingLine(set):
    """
    A `set` subclass which contains the users who reacted with the given ``Emoji`` on a ``Message``.
    
    Attributes
    ----------
    unknown : `int`
        The amount of not known reactors.
    """
    __slots__ = ('unknown',)
    
    if NEEDS_DUMMY_INIT:
        def __init__(self, *args, **kwargs):
            pass
    else:
        __init__ = object.__init__
    
    
    def __new__(cls, initialize_with = None, unknown = None):
        """
        Creates a new reaction mapping line
        
        Parameters
        ----------
        initialize_with : `None`, `iterable` of (`None`, ``ClientUserBase``), `instance<reaction_mapping_line_type>` \
                = `None`, Optional
            The value ot initialize the line with.
        unknown : `None, `int` = `None`, Optional
            The given `unknown` value to initialize the reaction line with.
        
        Raises
        ------
        TypeError
            - If a parameter's type is not acceptable.
        ValueError
            - If a parameter's value is not acceptable.
        """
        validated_line, validated_unknown = _validate_reaction_mapping_line_initialise_with(cls, initialize_with)
        validated_unknown += _validate_reaction_mapping_line_unknown(unknown)
        
        self = set.__new__(cls)
        self.unknown = validated_unknown
        
        if (validated_line is not None):
            set.update(self, validated_line)
        
        return self
    
    
    @classmethod
    def _create_empty(cls, unknown):
        """
        Creates a new reaction mapping line.
        
        Parameters
        ----------
        unknown : `int`
            The amount of not known reactors.
        
        Returns
        -------
        self : instance<cls>
        """
        self = set.__new__(cls)
        self.unknown = unknown
        return self
    
    
    def __len__(self):
        """Returns the amount of users, who reacted with the given emoji on the respective message."""
        return set.__len__(self) + self.unknown
    
    
    def __repr__(self):
        """Returns the representation of the container."""
        repr_parts = [
            self.__class__.__name__,
            '({',
        ]
        
        # set indexing is not public, so we need to do a check, like this
        if set.__len__(self):
            for user in self:
                repr_parts.append(repr(user))
                repr_parts.append(', ')
            
            repr_parts[-1] = '}'
        else:
            repr_parts.append('}')
        
        unknown = self.unknown
        if unknown:
            repr_parts.append(', unknown = ')
            repr_parts.append(repr(unknown))
        
        repr_parts.append(')')
        
        return ''.join(repr_parts)
    
    
    def __bool__(self):
        """Returns whether self has any elements."""
        if self.unknown:
            return True
        
        if set.__len__(self):
            return True
        
        return False
    
    
    def __eq__(self, other):
        """Returns whether self equals to other."""
        if type(self) is type(other):
            return self._is_equal_same_type(other)
            
        if (getattr(other, '__iter__', None) is not None):
            return self._is_equal_iterable(other)
        
        return NotImplemented
    
    def _is_equal_same_type(self, other):
        """
        Returns whether self equals to other. `other` must be same type as self.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other reaction mapping line to compare self to.
        
        Returns
        -------
        is_equal : `bool`
        """
        if self.unknown != other.unknown:
            return False
        
        if not set.__eq__(self, other):
            return False
        
        return True
    
    
    def _is_equal_iterable(self, other):
        """
        Returns whether self equals to other, where other is an iterable.
        
        Parameters
        ----------
        other : `iterable` of (`None`, ``ClientUserBase``)
            The other object to compare self to.
        
        Returns
        -------
        is_equal : `NotImplemented`, `bool`
        """
        unknown = 0
        users = set()
        
        for user in other:
            if user is None:
                unknown += 1
                continue
            
            if isinstance(user, ClientUserBase):
                users.add(user)
                continue
            
            return NotImplemented
        
        
        if self.unknown != unknown:
            return False
        
        if not set.__eq__(self, users):
            return False
        
        return True
    
    
    def __hash__(self):
        """
        Returns the hash value of reaction mapping line.
        > Note that it is the current hash of the object and can change by changing the object.
        """
        hash_value = 0
        
        unknown = self.unknown
        hash_value ^= unknown << (1 + (unknown % 13))
        
        for user in set.__iter__(self):
            hash_value ^= hash(user)
        
        return hash_value
    
    
    @classmethod
    def _create_full(cls, users):
        """
        Creates a new ``ReactionMappingLine`` with the given users with `.unknown` set to `0`.
        
        Parameters
        ----------
        users : `list` of ``ClientUserBase``
            A `list`, which should already contain all the users of the reaction mapping line.

        Returns
        -------
        self : ``ReactionMappingLine``
        """
        self = set.__new__(cls)
        self.unknown = 0
        set.update(self, users)
        return self
    
    
    def update(self, users):
        """
        Updates the reaction mapping line with the given users.
        
        Parameters
        ----------
        users : `list` of ``ClientUserBase``
            A `list` of users, who reacted on the respective `Message` with the respective ``Emoji``.
        """
        length_old = len(self)
        set.update(self, users)
        length_new = len(self)
        
        unknown = self.unknown - (length_new - length_old)
        if (unknown < 0):
            unknown = 0
        self.unknown = unknown
    
    
    def copy(self):
        """
        Copies the reaction mapping line.
        
        Returns
        -------
        new : ``ReactionMappingLine``
        """
        new = set.__new__(type(self))
        set.__init__(new, self)
        new.unknown = self.unknown
        return new
    
    
    def filter_after(self, limit, after):
        """
        If we know all the reactors, then instead of executing a Discord API request we filter the reactors locally
        using this method.
        
        Parameters
        ----------
        limit : `int`
            The maximal limit of the users to return.
        after : `int`
            Gets the users after this specified id.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        return sorted([user for user in set.__iter__(self) if user.id > after])[:limit]
    
    
    def clear(self):
        """
        Clears the reaction mapping line by removing every ``User`` object from it.
        """
        clients = []
        for user in self:
            if isinstance(user, Client):
                clients.append(user)

        self.unknown += (set.__len__(self) - len(clients))
        set.clear(self)
        set.update(self, clients)
    
    
    def remove(self, user):
        """
        Removes the given user from self.
        
        Parameters
        ----------
        user : ``ClientUserBase``
            The user to remove.
        
        Returns
        -------
        success : `bool`
            Whether the user was successfully removed.
        """
        try:
            set.remove(self, user)
        except KeyError:
            unknown = self.unknown
            if unknown > 0:
                self.unknown = unknown - 1
                success = True
            
            else:
                success = False
        
        else:
            success = True
        
        return success
