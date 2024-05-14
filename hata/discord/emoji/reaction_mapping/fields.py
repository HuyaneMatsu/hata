__all__ = ()

from ..reaction_mapping_line import ReactionMappingLine

from ..emoji import Emoji
from ..parsing import parse_reaction
from ..reaction import Reaction, ReactionType


def validate_reaction(reaction):
    """
    Validates whether the given reaction value.
    
    Parameters
    ----------
    reaction : ``Emoji``, ``Reaction``, `str`
        The reaction to validate.
    
    Returns
    -------
    reaction : ``Reaction``
    
    Raises
    ------
    TypeError
        - If `reaction`'s type is incorrect.
    """
    if isinstance(reaction, Reaction):
        return reaction
    
    if isinstance(reaction, Emoji):
        return Reaction.from_fields(reaction, ReactionType.standard)
    
    if isinstance(reaction, str):
        emoji = parse_reaction(reaction)
        if emoji is not None:
            return Reaction.from_fields(emoji, ReactionType.standard)
        
        raise ValueError(
            f'`reaction` is given as `str`, but could not parse it. Got {reaction!r}.'
        )
    
    raise TypeError(
        f'Reaction can be `{Reaction.__name__}`, `{Emoji.__name__}`, `str`, '
        f'got {reaction.__class__.__name__}; {reaction!r}.'
    )


def validate_reaction_mapping_line(reaction_mapping_line):
    """
    Validates the given `reaction_mapping_line` value.
    
    Parameters
    ----------
    reaction_mapping_line : ``ReactionMappingLine``
        The reaction mapping line to validate.
    
    Returns
    -------
    reaction_mapping_line : ``ReactionMappingLine``
    
    Raises
    ------
    TypeError
        - If `reaction_mapping_line`'s type is incorrect.
    """
    if not isinstance(reaction_mapping_line, ReactionMappingLine):
        raise TypeError(
            f'Reaction mapping line can be can be `{ReactionMappingLine.__name__}`, '
            f'got {type(reaction_mapping_line).__name__}; {reaction_mapping_line!r}.'
        )
    
    return reaction_mapping_line


def validate_lines(lines):
    """
    Validates a reaction mapping's lines.
    
    Parameters
    ----------
    lines : `None | dict<str | Emoji | Reaction, ReactionMappingLine> \
            | list<(str | Emoji | Reaction, ReactionMappingLine)>`
        The value to initialise the reaction mapping.
    
    Returns
    -------
    built_lines : `None`, `list` of `tuple` ((``Emoji``, ``Reaction``), ``ReactionMappingLine``) items
        The validated extend with value.
    
    Raises
    ------
    TypeError
        - If `lines`'s type is unacceptable.
        - If an item (or element) of `lines` has incorrect type, length or structure.
    """
    if lines is None:
        built_lines = None
    
    elif isinstance(lines, dict):
        built_lines = None
        for item in lines.items():
            built_lines = _validate_reaction_mapping_lines_item(built_lines, item)
    
    elif (getattr(lines, '__iter__', None) is not None):
        built_lines = None
        
        for item in lines:
            if not isinstance(item, tuple):
                raise TypeError(
                    f'`lines` items can be `tuple` instances, got '
                    f'{item.__class__.__name__}; {item!r}; lines = {lines!r}.'
                )
            
            item_length = len(item)
            if len(item) != 2:
                raise TypeError(
                    f'`lines` items can be `tuple` with length of `2`, got '
                    f'item_length = {item_length!r}; item = {item!r}; lines = {lines!r}.'
                )
            
            built_lines = _validate_reaction_mapping_lines_item(built_lines, item)
        
    else:
        raise TypeError(
            f'`lines` can be `None`, `iterable` or `dict`, got '
            f'{type(lines).__name__}; {lines!r}'
        )
    
    return built_lines


def _validate_reaction_mapping_lines_item(built_lines, item):
    """
    Validates an item of the `lines` parameter of ``ReactionMapping``.
    
    Parameters
    ----------
    built_lines : `None | dict<Reaction, ReactionMappingLine>`
        The validated extend with value.
    item : `(str | Emoji | Reaction, ReactionMappingLine)`
        Reaction mapping item to validate.
    
    Returns
    -------
    built_lines : `None | dict<Reaction, ReactionMappingLine>`
        The validated extend with value.
    
    Raises
    ------
    TypeError
        - If `item[0]` is not `str` / ``Emoji`` / ``Reaction``.
        - If `item[1]` is not ``ReactionMappingLine``.
    """
    reaction, line = item
    
    reaction = validate_reaction(reaction)
    line = validate_reaction_mapping_line(line)
    
    if line.count:
        if built_lines is None:
            built_lines = {}
        
        built_lines[reaction] = line
    
    return built_lines
