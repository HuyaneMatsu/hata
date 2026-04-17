import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Reaction, ReactionMapping, ReactionMappingLine, ReactionType
from ....user import User

from ..fields import validate_reactions



def _iter_options__passing():
    reactions = ReactionMapping()
    
    yield None, None
    yield reactions, reactions
    

def _iter_options__type_error():
    yield 12.6


def _iter_options__conversion():
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['x']
    
    user_id_0 = 202305010021
    user_id_1 = 202305010022
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    yield (
        {
            emoji_0: ReactionMappingLine(count = 2, users = [user_0, user_1]),
            emoji_1: ReactionMappingLine(count = 1, users = [user_1]),
        },
        ReactionMapping(
            lines = {
                Reaction.from_fields(emoji_0, ReactionType.standard): ReactionMappingLine(count = 2, users = [user_0, user_1]),
                Reaction.from_fields(emoji_1, ReactionType.standard): ReactionMappingLine(count = 1, users = [user_1]),
            }
        )
    )


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__conversion()).returning_last())
def test__validate_reactions(input_value):
    """
    Tests whether ``validate_reactions`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``ReactionMapping``
    
    Raises
    ------
    TypeError
    """
    output = validate_reactions(input_value)
    vampytest.assert_instance(output, ReactionMapping, nullable = True)
    return output
