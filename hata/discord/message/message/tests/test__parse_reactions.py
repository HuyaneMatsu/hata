import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Reaction, ReactionMapping, ReactionMappingLine, ReactionType 
from ....user import User

from ..fields import parse_reactions


def _iter_options():
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['x']
    
    user_id_0 = 202305010019
    user_id_1 = 202305010020
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    
    yield (
        {},
        None,
        None,
    )
    
    yield (
        {'reactions': None},
        None,
        None,
    )
    
    yield (
        {'reactions': []},
        None,
        None,
    )
    
    yield (
        {},
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2),
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 2),
            },
        ),
        ReactionMapping()
    )
    
    yield (
        {},
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2),
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 2),
            },
        ),
        ReactionMapping()
    )
    
    yield (
        {
            'reactions': ReactionMapping(
                lines = {
                    Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2),
                    Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 2),
                },
            ).to_data(),
        },
        None,
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2),
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 2),
            },
        )
    )
    yield (
        {
            'reactions': ReactionMapping(
                lines = {
                    Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2),
                    Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 2),
                },
            ).to_data(),
        },
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_0, user_1]),
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_1]),
            },
        ),
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_0, user_1]),
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 2),
            },
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_reactions(input_data, old_reactions):
    """
    Tests whether ``parse_reactions`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    old_reactions : `None | ReactionMapping`
        Old reactions if available.
    
    Returns
    -------
    output : `None | ReactionMapping`
    """
    if (old_reactions is not None):
        old_reactions = old_reactions.copy()
    
    output = parse_reactions(input_data, old_reactions)
    vampytest.assert_instance(output, ReactionMapping, nullable = True)
    return output
