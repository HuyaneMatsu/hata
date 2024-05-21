__all__ = ('ReactionMapping', )

from warnings import warn

from scarletio import RichAttributeErrorBaseType

from ..emoji import Emoji, create_partial_emoji_data, create_partial_emoji_from_data
from ..reaction import Reaction, ReactionType
from ..reaction_mapping_line import ReactionMappingLine

from .fields import validate_lines


COUNT_KEYS_TO_TYPES = (
    ('normal', ReactionType.standard),
    ('burst', ReactionType.burst),
)


class ReactionMapping(RichAttributeErrorBaseType):
    """
    Contains the reactions on a ``Message`` with (``Reaction``, ``ReactionMappingLine``) items.
    
    Attributes
    ----------
    lines : `None | dict<Reaction, ReactionMappingLine>`
        Reaction to users relation.
    """
    __slots__ = ('lines',)
    
    def __new__(cls, *, lines = ...):
        """
        Creates a new reaction mapping instance.
        
        Parameters
        ----------
        lines : `None | dict<str | Emoji | Reaction, ReactionMappingLine> \
                | list<(str | Emoji | Reaction, ReactionMappingLine)>`, Optional (Keyword only)
            Reaction to users relation.
        
        Raises
        ------
        TypeError
            - If `initialize_with`'s is unacceptable.
        """
        if lines is ...:
            lines = None
        else:
            lines = validate_lines(lines)
        
        # Construct
        self = object.__new__(cls)
        self.lines = lines
        return self
    
    
    def __len__(self):
        """Returns the length of the reaction mapping."""
        lines = self.lines
        if lines is None:
            return 0
        
        return len(lines)
    
    
    def __bool__(self):
        """Returns whether self has any any reactions"""
        
        # lines
        lines = self.lines
        if (lines is not None) and lines:
            return True
        
        return False
    
    
    def __repr__(self):
        """Returns the reaction mapping's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # lines
        lines = self.lines
        if (lines is not None) and lines:
            repr_parts.append('lines = ')
            repr_parts.append(repr(lines))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether self equals to other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # lines
        self_lines = self.lines
        other_lines = other.lines
        if (self_lines is None) or (not self_lines):
            if (other_lines is not None) and other_lines:
                return False
        
        else:
            if (other_lines is None) or (not other_lines):
                return False
            
            if self_lines != other_lines:
                return False
        
        return True
    
    
    def __hash__(self):
        """
        Returns the hash value of reaction mapping line.
        > Note that it is the current hash of the object and can change by changing the object.
        """
        hash_value = 0
        
        lines = self.lines
        if (lines is not None):
            for reaction, line in lines.items():
             hash_value ^= hash(reaction) & hash(line)
        
        return hash_value
    
    
    @classmethod
    def from_data(cls, data):
        """
        Fills the reaction mapping with the given data.
        
        Parameters
        ----------
        data : `None`, `list<dict<str, object>>`
            Reactions data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        lines = None
        
        for line_data in data:
            counts = line_data.get('count_details', None)
            if counts is None:
                continue
            
            emoji = create_partial_emoji_from_data(line_data['emoji'])
            
            for key, reaction_type in COUNT_KEYS_TO_TYPES:
                count = counts.get(key, 0)
                if not count:
                    continue
                
                if lines is None:
                    lines = {}
                
                line = ReactionMappingLine._create_empty()
                line.count = count
                lines[Reaction.from_fields(emoji, reaction_type)] = line
        
        # Construct
        self = object.__new__(cls)
        self.lines = lines
        return self
    
    
    def to_data(self):
        """
        Tries to convert the reactions back to a json serializable list.
        
        Returns
        -------
        data : `list<dict<str, object>>`
        """
        data = []
        
        lines = self.lines
        if (lines is not None):
            reduced_to_emojis = {}
            for reaction, line in lines.items():
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
                    counts[key] = 0 if (line is None) else line.count
                
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
        lines = self.lines
        if lines is None:
            return 0
        
        return len({reaction.emoji for reaction in lines.keys()})
    
    
    @property
    def reaction_count(self):
        """
        The amount of different reactions, which were added on the reaction mapping's respective ``Message``.
        
        Returns
        -------
        reaction_count : `int`
        """
        lines = self.lines
        if lines is None:
            return 0
        
        return len(lines)
    
    
    @property
    def total_count(self):
        """
        The total amount reactions given on the reaction mapping's respective message.
        
        Returns
        -------
        total_count : `int`
        """
        lines = self.lines
        if lines is None:
            return 0
        
        return sum(line.count for line in lines.values())
    
    
    def copy(self):
        """
        Copies the reaction mapping returning a new one.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        # lines
        lines = self.lines
        if (lines is not None):
            lines = {reaction.copy(): line.copy() for reaction, line in lines.items()}
        new.lines = lines
        
        return new
    
    
    def _add_reaction(self, reaction, user):
        """
        Adds a user to the reactors.
        
        Parameters
        ----------
        reaction : ``Reaction``
            The reaction.
        user : ``ClientUserBase``
            The reactor user.
        
        Returns
        -------
        success : `bool`
        """
        line = self._get_or_create_line(reaction)
        return line._add_reaction(user)
    
    
    def _remove_reaction(self, reaction, user):
        """
        Removes a user from the reactors.
        
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
        lines = self.lines
        if lines is None:
            return False
        
        try:
            line = lines[reaction]
        except KeyError:
            return False
        
        success = line._remove_reaction(user)
        if success:
            if not line.count:
                del lines[reaction]
        
        return success
    
    
    def _remove_reaction_emoji(self, emoji):
        """
        Removes all the users who reacted with the given ``Emoji`` and then returns the stored line.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji to remove.
        
        Returns
        -------
        removed_lines : `None | dict<Reaction, ReactionMappingLine>`
        """
        removed_lines = None
        
        lines = self.lines
        if (lines is not None):
            for reaction, line in lines.items():
                if reaction.emoji is not emoji:
                    continue
            
                if removed_lines is None:
                    removed_lines = {}
            
                removed_lines[reaction] = line
                continue
        
            if (removed_lines is not None):
                for reaction in removed_lines.keys():
                    del lines[reaction]
            
        return removed_lines
    
    
    def _fill_some_reactions(self, reaction, users):
        """
        Called when some reactors of a reaction are updated.
        
        Parameters
        ----------
        reaction : ``Reaction``
            The reaction, which users' are updated.
        users : `list` of ``ClientUserBase``
            The added reactors.
        """
        line = self._get_or_create_line(reaction)
        line._fill_some_reactions(users)
    
    
    def _fill_all_reactions(self, reaction, users):
        """
        Called when all the reactors of a reaction are updated of the reaction mapping.
        
        Parameters
        ----------
        reaction : ``Reaction``
            The reaction, which users' are updated.
        users : `list` of ``ClientUserBase``
            The added reactors.
        """
        line = self._get_or_create_line(reaction)
        line._fill_all_reactions(users)
    
    
    def __getitem__(self, reaction):
        """
        Gets the result for the given answer.
        
        Parameters
        ----------
        reaction : `Emoji | Reaction`
            
        Returns
        -------
        result : `None | ReactionMappingLine`
       
        """
        lines = self.lines
        if (lines is not None):
            return lines.get(reaction, None)
    
    
    def _get_or_create_line(self, reaction):
        """
        Gets the line for the given `reaction`. If not found creates a new one.
        
        Parameters
        ----------
        reaction : ``Reaction``
            The reaction pointing at the line.
        
        Returns
        -------
        line : ``ReactionMappingLine``
        """
        lines = self.lines
        if lines is None:
            line = ReactionMappingLine._create_empty()
            self.lines = {reaction: line}
        else:
            try:
                line = lines[reaction]
            except KeyError:
                line = ReactionMappingLine._create_empty()
                lines[reaction] = line
        
        return line
    
    
    def clear(self):
        """
        Clears the non-client users of the reaction mapping.
        """
        lines = self.lines
        if (lines is not None):
            lines.clear()
    
    
    def __contains__(self, reaction):
        """Returns whether the reaction mapping has the given reaction."""
        lines = self.lines
        if lines is None:
            return False
        
        return reaction in lines
    
    
    def iter_reactions(self):
        """
        Iterates over reactions.
        
        This method is an iterable generator.
        
        Yields
        ------
        reaction : ``Reaction``
        """
        lines = self.lines
        if (lines is not None):
            yield from lines.keys()
    
    
    def iter_lines(self):
        """
        Iterates over lines.
        
        This method is an iterable generator.
        
        Yields
        ------
        item : ``ReactionMappingLine``
        """
        lines = self.lines
        if (lines is not None):
            yield from lines.values()
    
    
    def iter_items(self):
        """
        Iterates over `reaction - lines` pairs.
        
        This method is an iterable generator.
        
        Yields
        ------
        item : `(Reaction, ReactionMappingLine)`
        """
        lines = self.lines
        if (lines is not None):
            yield from lines.items()
    
    
    
    @property
    def fully_loaded(self):
        """
        Returns whether the reaction mapping line is fully loaded.
        
        Deprecated and will be removed in 2025 Jan.
        """
        warn(
            (
                f'`{type(self).__name__}.fully_loaded` is deprecated and will be removed in 2025 Jan.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        for result in self.iter_result():
            if result.unknown:
                return False
        
        return True
    
    
    def keys(self):
        """
        Deprecated and will be removed in 2025 Jan. Use ``.iter_reactions`` instead.
        """
        warn(
            (
                f'`{type(self).__name__}.keys` is deprecated and will be removed in 2025 Jan. '
                f'Use `.iter_reactions` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.iter_reactions()


    def values(self):
        """
        Deprecated and will be removed in 2025 Jan. Use ``.iter_lines`` instead.
        """
        warn(
            (
                f'`{type(self).__name__}.values` is deprecated and will be removed in 2025 Jan. '
                f'Use `.iter_lines` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.iter_lines()


    def items(self):
        """
        Deprecated and will be removed in 2025 Jan. Use ``.iter_items`` instead.
        """
        warn(
            (
                f'`{type(self).__name__}.items` is deprecated and will be removed in 2025 Jan. '
                f'Use `.iter_items` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.iter_items()
