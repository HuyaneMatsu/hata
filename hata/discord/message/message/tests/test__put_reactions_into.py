import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Reaction, ReactionMapping, ReactionMappingLine, ReactionType

from ..fields import put_reactions_into


def _iter_options():
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['x']

    reaction_mapping = ReactionMapping(
        lines = {
            Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2),
            Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1),
        }
    )
    
    yield None, False, {}
    yield None, True, {'reactions': []}
    yield reaction_mapping, False, {'reactions': reaction_mapping.to_data()}
    yield reaction_mapping, True, {'reactions': reaction_mapping.to_data()}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_reactions_into(input_value, defaults):
    """
    Tests whether ``put_reactions_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | ReactionMapping`
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_reactions_into(input_value, {}, defaults)
