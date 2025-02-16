__all__ = ()

from ...field_parsers import functional_parser_factory
from ...field_putters import functional_putter_factory
from ...field_validators import entity_validator_factory, preinstanced_validator_factory

from ..emoji import Emoji, create_partial_emoji_data, create_partial_emoji_from_data

from .preinstanced import ReactionType


# emoji

parse_emoji = functional_parser_factory('emoji', create_partial_emoji_from_data)
put_emoji = functional_putter_factory('emoji', create_partial_emoji_data)
validate_emoji = entity_validator_factory('emoji', Emoji)

# type

def parse_type(data):
    """
    Parses out the reaction's type the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Reaction data.
    
    Returns
    -------
    reaction_type : ``ReactionType``
    """
    if data.get('burst', False):
        return ReactionType.burst
    
    return ReactionType.standard


def put_type(reaction_type, data, defaults):
    """
    Puts the reaction's type into the given `data` json serializable object.
    
    Parameters
    ----------
    reaction_type : ``ReactionType``
        The reaction's type.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if reaction_type is ReactionType.burst:
        burst_field_value = True
    else:
        burst_field_value = False
        
    data['burst'] = burst_field_value
    return data


validate_type = preinstanced_validator_factory('reaction_type', ReactionType)
