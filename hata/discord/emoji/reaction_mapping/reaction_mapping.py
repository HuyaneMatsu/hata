__all__ = ('ReactionMapping', )

from scarletio import set_docs
from scarletio.utils.compact import NEEDS_DUMMY_INIT

from ..emoji import Emoji, create_partial_emoji_data, create_partial_emoji_from_data
from ..reaction import Reaction, ReactionType

from .fields import validate_reaction
from .reaction_mapping_line import ReactionMappingLine


COUNT_KEYS_TO_TYPES = (
    ('normal', ReactionType.standard),
    ('burst', ReactionType.burst),
)


def _validate_reaction_mapping_initialize_with(reaction_mapping_type, initialize_with):
    """
    Validates the `initialize_with` parameter of ``ReactionMapping``.
    
    Parameters
    ----------
    reaction_mapping_type : `type`
        The type of the reaction mapping.
    initialize_with : `None`, `iterable` of `tuple` ((``Emoji``, ``Reaction``), `iterable` of \
            (``ClientUserBase``, `None`)), `dict` of \ ((``Emoji``, ``Reaction``), `iterable` of \
            (``ClientUserBase``, `None`) items, `instance<reaction_mapping_type>`
        The value to initialise the reaction mapping.
    
    Returns
    -------
    built_initialize_with : `None`, `list` of `tuple` ((``Emoji``, ``Reaction``), ``ReactionMappingLine``) items
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
    built_initialize_with : `None`, `list` of `tuple` ((``Emoji``, ``Reaction``), ``ReactionMappingLine``) items
        The validated extend with value.
    """
    built_initialize_with = None
    
    for reaction, line in initialize_with.items():
        if built_initialize_with is None:
            built_initialize_with = []
        
        built_initialize_with.append((reaction, line.copy()))
    
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
    built_initialize_with : `None`, `list` of `tuple` ((``Emoji``, ``Reaction``), ``ReactionMappingLine``) items
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
    initialize_with : `iterable` of `tuple` ((``Emoji``, ``Reaction``), `iterable` of (``ClientUserBase``, `None`))
        The value to initialize_with self with.
    
    Returns
    -------
    built_initialize_with : `None`, `list` of `tuple` ((``Emoji``, ``Reaction``), ``ReactionMappingLine``) items
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
                f'item_length = {item_length!r}; item = {item!r}; initialize_with{initialize_with!r}'
            )
        
        built_initialize_with = _validate_reaction_mapping_initialize_with_item(built_initialize_with, item)
    
    return built_initialize_with


def _validate_reaction_mapping_initialize_with_item(built_initialize_with, item):
    """
    Validates an item of the `initialize_with` parameter of ``ReactionMapping``.
    
    Parameters
    ----------
    built_initialize_with : `None`, `list` of `tuple` ((``Emoji``, ``Reaction``), ``ReactionMappingLine``) items
        The validated extend with value.
    item : `tuple` (``Emoji``, `iterable` of (``ClientUserBase``, `None`))
        Reaction mapping item to validate.
    
    Returns
    -------
    built_initialize_with : `None`, `list` of `tuple` ((``Emoji``, ``Reaction``), ``ReactionMappingLine``) items
        The validated extend with value.
    
    Raises
    ------
    TypeError
        - If `item[0]` is not ``Emoji`` / ``Reaction``.
        - If `item[1]` isn ot accepted by ``ReactionMappingLine``.
    """
    reaction, line = item
    
    reaction = validate_reaction(reaction)
    line = ReactionMappingLine(line)
    
    if line:
        if built_initialize_with is None:
            built_initialize_with = []
        
        built_initialize_with.append((reaction, line))
    
    return built_initialize_with


class ReactionMapping(dict):
    """
    A `dict` subclass, which contains the reactions on a ``Message`` with (``Reaction``, ``ReactionMappingLine``)
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
    
    
    def __new__(cls, initialize_with = None):
        """
        Creates a new reaction mapping instance.
        
        Parameters
        ----------
        initialize_with : `None`, `iterable` of `tuple` ((``Emoji``, ``Reaction``), `iterable` of \
                (``ClientUserBase``, `None`)), `dict` of \ ((``Emoji``, ``Reaction``), `iterable` of \
                (``ClientUserBase``, `None`) items, `instance<cls>` = `None`, Optional
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
            for reaction, line in dict.items(self):
                repr_parts.append(repr(reaction))
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
        for reaction in other.keys():
            if not isinstance(reaction, (Emoji, Reaction)):
                return NotImplemented
        
        is_equal = True
        
        for reaction in {*dict.keys(self), *other.keys()}:
            try:
                other_line = other[reaction]
            except KeyError:
                is_equal = False
                continue
            
            try:
                self_line = self[reaction]
            except KeyError:
                self_line = ReactionMappingLine._create_empty(0)
                is_equal = False
            
            line_equals = type(self_line).__eq__(self_line, other_line)
            if line_equals is NotImplemented:
                return NotImplemented
            
            if not line_equals:
                is_equal = False
            continue
        
        return is_equal
    
    
    def __hash__(self):
        """
        Returns the hash value of reaction mapping line.
        > Note that it is the current hash of the object and can change by changing the object.
        """
        hash_value = 0
        
        for reaction, line in dict.items(self):
            hash_value ^= hash(reaction) & hash(line)
        
        return hash_value
    
    
    @classmethod
    def from_data(cls, data):
        """
        Fills the reaction mapping with the given data.
        
        Parameters
        ----------
        data : `None`, `dict` of (`str`, `object`) items
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
            counts = line_data.get('count_details', None)
            if counts is None:
                continue
            
            emoji = create_partial_emoji_from_data(line_data['emoji'])
            
            for key, reaction_type in COUNT_KEYS_TO_TYPES:
                count = counts.get(key, 0)
                if count:
                    self[Reaction.from_fields(emoji, reaction_type)] = ReactionMappingLine._create_empty(count)
        
        return self
    
    
    def to_data(self):
        """
        Tries to convert the reactions back to a json serializable list.
        
        Returns
        -------
        data : `list<dict<str, object>>`
        """
        data = []
        
        reduced_to_emojis = {}
        for reaction, line in dict.items(self):
            emoji = reaction.emoji
            try:
                by_type = reduced_to_emojis[emoji]
            except KeyError:
                by_type = {}
                reduced_to_emojis[emoji] = by_type
            
            by_type[reaction.type] = line
            
            
        for emoji, by_type in reduced_to_emojis.items():
            counts = {}
            
            for key, reaction_type in COUNT_KEYS_TO_TYPES:
                line = by_type.get(reaction_type, None)
                counts[key] = 0 if (line is None) else len(line)
            
            data.append({
                'count_details': counts,
                'emoji': create_partial_emoji_data(emoji),
            })
        
        return data
    
    
    @property
    def emoji_count(self):
        """
        The amount of different emojis, which were added on the reaction mapping's respective ``Message``.
        
        Returns
        -------
        emoji_count : `int`
        """
        return len({reaction.emoji for reaction in dict.keys(self)})
    
    
    reaction_count = set_docs(
        property(dict.__len__),
        """
        The amount of different reactions, which were added on the reaction mapping's respective ``Message``.
        
        Returns
        -------
        reaction_count : `int`
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
    
    
    def copy(self):
        """
        Copies the reaction mapping returning a new one.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = dict.__new__(type(self))
        new.fully_loaded = self.fully_loaded
        
        for reaction, line in dict.items(self):
            new[reaction.copy()] = line.copy()
        
        return new
    
    
    def add(self, reaction, user):
        """
        Adds a user to the reactors.
        
        Parameters
        ----------
        reaction : ``Reaction``
            The reaction.
        user : ``ClientUserBase``
            The reactor user.
        """
        try:
            line = self[reaction]
        except KeyError:
            line = ReactionMappingLine._create_empty(0)
            self[reaction] = line
        
        line.add(user)
    
    
    def remove(self, reaction, user):
        """
        Removes a user to the reactors.
        
        Parameters
        ----------
        reaction : ``Reaction``
            The reaction.
        user : ``ClientUserBase``
            The removed reactor user.
        
        Returns
        -------
        success : `bool`
        """
        try:
            line = self[reaction]
        except KeyError:
            return False
        
        success = line.remove(user)
        if success:
            if not line:
                del self[reaction]
        
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
        line : `None`, `dict<Reaction, ReactionMappingLine>`
        """
        lines = None
        
        for reaction, line in dict.items(self):
            if reaction.emoji is not emoji:
                continue
            
            if lines is None:
                lines = {}
            
            lines[reaction] = line
            continue
        
        if lines is not None:
            should_full_check = False
            
            for reaction, line in lines.items():
                del self[reaction]
                
                if line.unknown:
                    should_full_check = True
            
            if should_full_check:
                self._full_check()
        
        return lines
    
    
    # this function is called if a reaction loses all it's unknown reactors
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
    
    
    # we call this when we get SOME reactors of a reaction
    def _update_some_users(self, reaction, users):
        """
        Called when some reactors of a reaction are updated.
        
        Parameters
        ----------
        reaction : ``Reaction``
            The reaction, which users' are updated.
        users : `list` of ``ClientUserBase``
            The added reactors.
        """
        try:
            line = self[reaction]
        except KeyError:
            line = ReactionMappingLine._create_empty(0)
            self[reaction] = line
            
        line.update(users)
        self._full_check()
    
    
    def _update_all_users(self, reaction, users):
        """
        Called when all the reactors of a reaction are updated of the reaction mapping.
        
        Parameters
        ----------
        reaction : ``Reaction``
            The reaction, which users' are updated.
        users : `list` of ``ClientUserBase``
            The added reactors.
        """
        self[reaction] = ReactionMappingLine._create_full(users)
        self._full_check()
