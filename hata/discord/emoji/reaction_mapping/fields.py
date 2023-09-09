__all__ = ()

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
