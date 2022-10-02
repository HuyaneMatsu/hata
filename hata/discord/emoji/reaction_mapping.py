__all__ = ('ReactionMapping', )

from scarletio import set_docs
from scarletio.utils.compact import NEEDS_DUMMY_INIT

from .emoji import Emoji
from .reaction_mapping_line import ReactionMappingLine
from .utils import create_partial_emoji_data, create_partial_emoji_from_data


def _validate_reaction_mapping_initialize_with(reaction_mapping_type, initialize_with):
    """
    Validates the `initialize_with` parameter of ``ReactionMapping``.
    
    Parameters
    ----------
    reaction_mapping_type : `type`
        The type of the reaction mapping.
    initialize_with : `None`, `iterable` of `tuple` (``Emoji``, `iterable` of (``ClientUserBase``, `None`)), `dict` of \
            (``Emoji``, `iterable` of (``ClientUserBase``, `None`) items, `instance<reaction_mapping_type>`
        The value to initialise the reaction mapping.
    
    Returns
    -------
    built_initialize_with : `None`, `list` of `tuple` (``Emoji``, ``ReactionMappingLine``) items
        The validated extend with value.
    
    Raises
    ------
    TypeError
        - If `initialize_with`'s type is unacceptable.
        - If an item (or element) of `initialize_with` has incorrect type, length or structure.
    """
    if initialize_with is None:
        built_initialize_with = None
    
    elif type(initialize_with) is reaction_mapping_type:
        built_initialize_with = _validate_reaction_mapping_initialize_with_same(initialize_with)
    
    elif isinstance(initialize_with, dict):
        built_initialize_with = _validate_reaction_mapping_initialize_with_dict(initialize_with)
    
    elif (getattr(initialize_with, '__iter__', None) is not None):
        built_initialize_with = _validate_reaction_mapping_initialize_with_iterable(initialize_with)
    
    else:
        raise TypeError(
            f'`initialize_with` can be `None`, `{reaction_mapping_type.__name__}`, `iterable` or `dict`, got '
            f'{initialize_with.__class__.__name__}; {initialize_with!r}'
        )
    
    return built_initialize_with


def _validate_reaction_mapping_initialize_with_same(initialize_with):
    """
    Validates the `initialize_with` parameter of ``ReactionMapping`` where it is the same type.
    
    Parameters
    ----------
    initialize_with : ``ReactionMapping``
        The value to initialize_with self with.
    
    Returns
    -------
    built_initialize_with : `None`, `list` of `tuple` (``Emoji``, ``ReactionMappingLine``) items
        The validated extend with value.
    """
    built_initialize_with = None
    
    for emoji, line in initialize_with.items():
        if built_initialize_with is None:
            built_initialize_with = []
        
        built_initialize_with.append((emoji, line.copy()))
    
    return built_initialize_with


def _validate_reaction_mapping_initialize_with_dict(initialize_with):
    """
    Validates the `initialize_with` parameter of ``ReactionMapping`` where it is a dictionary.
    
    Parameters
    ----------
    initialize_with : `dict` of (``Emoji``, `iterable` of (``ClientUserBase``, `None`) items
        The value to initialize_with self with.
    
    Returns
    -------
    built_initialize_with : `None`, `list` of `tuple` (``Emoji``, ``ReactionMappingLine``) items
        The validated extend with value.
    
    Raises
    ------
    TypeError
        - If `initialize_with` has an item of an unacceptable structure.
    """
    built_initialize_with = None
    for item in initialize_with.items():
        built_initialize_with = _validate_reaction_mapping_initialize_with_item(built_initialize_with, item)
    
    return built_initialize_with


def _validate_reaction_mapping_initialize_with_iterable(initialize_with):
    """
    Validates the `initialize_with` parameter of ``ReactionMapping`` where it is any iterable.
    
    Parameters
    ----------
    initialize_with : `iterable` of `tuple` (``Emoji``, `iterable` of (``ClientUserBase``, `None`))
        The value to initialize_with self with.
    
    Returns
    -------
    built_initialize_with : `None`, `list` of `tuple` (``Emoji``, ``ReactionMappingLine``) items
        The validated extend with value.
    
    Raises
    ------
    TypeError
        - If `initialize_with` contains a non `tuple` element.
        - If `initialize_with` contains an element which length is not `2`.
        - If `initialize_with` has an element of an unacceptable structure.
    """
    built_initialize_with = None
    
    for item in initialize_with:
        if not isinstance(item, tuple):
            raise TypeError(
                f'`initialize_with` items can be `tuple` instances, got '
                f'{item.__class__.__name__}; {item!r}; initialize_with{initialize_with!r}'
            )
        
        item_length = len(item)
        if len(item) != 2:
            raise TypeError(
                f'`initialize_with` items can be `tuple` with length of `2`, got '
                f'item_length={item_length!r}; item={item!r}; initialize_with{initialize_with!r}'
            )
        
        built_initialize_with = _validate_reaction_mapping_initialize_with_item(built_initialize_with, item)
    
    return built_initialize_with


def _validate_reaction_mapping_initialize_with_item(built_initialize_with, item):
    """
    Validates an item of the `initialize_with` parameter of ``ReactionMapping``.
    
    Parameters
    ----------
    built_initialize_with : `None`, `list` of `tuple` (``Emoji``, ``ReactionMappingLine``) items
        The validated extend with value.
    item : `tuple` (``Emoji``, `iterable` of (``ClientUserBase``, `None`))
        Reaction mapping item to validate.
    
    Returns
    -------
    built_initialize_with : `None`, `list` of `tuple` (``Emoji``, ``ReactionMappingLine``) items
        The validated extend with value.
    
    Raises
    ------
    TypeError
        - If `item[0]` is not ``Emoji``.
        - If `item[1]` isn ot accepted by ``ReactionMappingLine``.
    """
    emoji, line = item
    
    if not isinstance(emoji, Emoji):
        raise TypeError(
            f'`item[0]` can be `{Emoji.__name__}` instance, got '
            f'{emoji.__class__.__name__}; {emoji!r}; item={item!r}.'
        )
    
    line = ReactionMappingLine(line)
    
    if line:
        if built_initialize_with is None:
            built_initialize_with = []
        
        built_initialize_with.append((emoji, line))
    
    return built_initialize_with


class ReactionMapping(dict):
    """
    A `dict` subclass, which contains the reactions on a ``Message`` with (``Emoji``, ``ReactionMappingLine``)
    items.
    
    Attributes
    ----------
    fully_loaded : `bool`
        Whether the reaction mapping line is fully loaded.
    """
    __slots__ = ('fully_loaded',)
    
    if NEEDS_DUMMY_INIT:
        def __init__(self, *args, **kwargs):
            pass
    else:
        __init__ = object.__init__
    
    
    def __new__(cls, initialize_with=None):
        """
        Creates a new reaction mapping instance.
        
        Parameters
        ----------
        initialize_with : `None`, `iterable` of `tuple` (``Emoji``, `iterable` of (``ClientUserBase``, `None`)), `dict` of \
                (``Emoji``, `iterable` of (``ClientUserBase``, `None`) items, `instance<cls>` = `None`, Optional
            The value to initialize_with self with.
        
        Raises
        ------
        TypeError
            - If `initialize_with`'s is unacceptable.
        """
        built_initialize_with = _validate_reaction_mapping_initialize_with(cls, initialize_with)
        
        self = dict.__new__(cls)
        self.fully_loaded = True
        
        if (built_initialize_with is not None):
            dict.update(self, built_initialize_with)
            self._full_check()
        
        return self
    
    
    def __bool__(self):
        """Returns whether self has any any reactions"""
        if dict.__len__(self):
            return True
        
        return False
    
    
    def __repr__(self):
        """Returns the reaction mapping's representation."""
        repr_parts = [self.__class__.__name__, '(']
        
        if dict.__len__(self):
            repr_parts.append('{')
            for emoji, line in dict.items(self):
                repr_parts.append(repr(emoji))
                repr_parts.append(': ')
                repr_parts.append(repr(line))
                repr_parts.append(', ')
            
            repr_parts[-1] = '}'
        
        repr_parts.append(')')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether self equals to other."""
        if type(other) is type(self):
            return dict.__eq__(self, other)
        
        if isinstance(other, dict):
            return self._is_equal_dict(other)
        
        return NotImplemented
    
    
    def _is_equal_dict(self, other):
        """
        Returns whether self equals to the given dictionary.
        
        Parameters
        ----------
        other : `dict` of (``Emoji``, `iterable` of (``ClientUserBase``, `None`)) items
            The other instance to compare self to.
        
        Returns
        -------
        is_equal : `bool`, `NotImplemented`
        """
        for emoji in other.keys():
            if not isinstance(emoji, Emoji):
                return NotImplemented
        
        is_equal = True
        
        for emoji in {*dict.keys(self), *other.keys()}:
            try:
                users = other[emoji]
            except KeyError:
                is_equal = False
                continue
            
            try:
                line = self[emoji]
            except KeyError:
                line = ReactionMappingLine._create_empty(0)
                is_equal = False
            
            line_equals = type(line).__eq__(line, users)
            if line_equals is NotImplemented:
                return NotImplemented
            
            if not line_equals:
                is_equal = False
            continue
        
        return is_equal
    
    
    @classmethod
    def from_data(cls, data):
        """
        Fills the reaction mapping with the given data.
        
        Parameters
        ----------
        data : `None`, `dict` of (`str`, `Any`) items
            Reactions data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = dict.__new__(cls)
        if (data is None) or (not data):
            self.fully_loaded = True
            return self
        
        self.fully_loaded = False
        for line_data in data:
            emoji = create_partial_emoji_from_data(line_data['emoji'])
            line = ReactionMappingLine._create_empty(line_data.get('count', 1))
            self[emoji] = line
        
        return self
    
    
    emoji_count = set_docs(
        property(dict.__len__),
        """
        The amount of different emojis, which were added on the reaction mapping's respective ``Message``.
        
        Returns
        -------
        emoji_count : `int`
        """
    )
    
    @property
    def total_count(self):
        """
        The total amount reactions given on the reaction mapping's respective message.
        
        Returns
        -------
        total_count : `int`
        """
        total_reactions = 0
        
        for users in dict.values(self):
            total_reactions += len(users)
        
        return total_reactions
    
    
    def clear(self):
        """
        Clears the reaction mapping with clearing it's lines.
        """
        for value in self.values():
            value.clear()
        
        if self.fully_loaded:
            self._full_check()
    
    
    def add(self, emoji, user):
        """
        Adds a user to the reactors.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The reacted emoji.
        user : ``ClientUserBase``
            The reactor user.
        """
        try:
            line = self[emoji]
        except KeyError:
            line = ReactionMappingLine._create_empty(0)
            self[emoji] = line
        
        line.add(user)
    
    
    def remove(self, emoji, user):
        """
        Removes a user to the reactors.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The removed reacted emoji.
        user : ``ClientUserBase``
            The removed reactor user.
        
        Returns
        -------
        success : `bool`
        """
        try:
            line = self[emoji]
        except KeyError:
            return False
        
        success = line.remove(user)
        if success:
            if not line:
                del self[emoji]
        
        return success
    
    
    def remove_emoji(self, emoji):
        """
        Removes all the users who reacted with the given ``Emoji`` and then returns the stored line.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji to remove.
        
        Returns
        -------
        line : `None`, ``ReactionMappingLine``
        """
        line = self.pop(emoji, None)
        if (line is not None) and line.unknown:
            self._full_check()
        
        return line
    
    
    # this function is called if an emoji loses all it's unknown reactors
    def _full_check(self):
        """
        Checks whether the reaction mapping is fully loaded, by checking it's values' `.unknown` and sets the current
        state to `.fully_loaded`.
        """
        for line in self.values():
            if line.unknown:
                self.fully_loaded = False
                return
        
        self.fully_loaded = True
    
    
    # we call this when we get SOME reactors of an emoji
    def _update_some_users(self, emoji, users):
        """
        Called when some reactors of an emoji are updated.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji, which users' are updated.
        users : `list` of ``ClientUserBase``
            The added reactors.
        """
        try:
            line = self[emoji]
        except KeyError:
            line = ReactionMappingLine._create_empty(0)
            self[emoji] = line
            
        line.update(users)
        self._full_check()
    
    
    def _update_all_users(self, emoji, users):
        """
        Called when all the reactors of an emoji are updated of the reaction mapping.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji, which users' are updated.
        users : `list` of ``ClientUserBase``
            The added reactors.
        """
        self[emoji] = ReactionMappingLine._create_full(users)
        self._full_check()
    
    
    def to_data(self):
        """
        Tries to convert the reactions back to a json serializable list.
        
        Returns
        -------
        data : `list` of `dict` of (`str`, `Any`)
        """
        data = []
        
        for emoji, users in dict.items(self):
            data.append({
                'count': len(users),
                'me': False, # Me is always False
                'emoji': create_partial_emoji_data(emoji),
            })
        
        return data
