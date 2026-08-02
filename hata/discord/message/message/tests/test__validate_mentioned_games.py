import vampytest

from ...mention_game import MentionGame

from ..fields import validate_mentioned_games


def _iter_options__passing():
    mention_game_0 = MentionGame.precreate(202607040019)
    mention_game_1 = MentionGame.precreate(202607040020)
    
    yield (
        None,
        None,
    )
    
    yield (
        [],
        None,
    )
    
    yield (
        [
            mention_game_0,
        ],
        (
            mention_game_0,
        ),
    )
    
    yield (
        [
            mention_game_1,
            mention_game_0,
        ],
        (
            mention_game_0,
            mention_game_1,
        ),
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_mentioned_games(input_value):
    """
    Validates whether ``validate_mentioned_games`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | tuple<MentionGame>``
    
    Raises
    ------
    TypeError
    """
    output = validate_mentioned_games(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, MentionGame)
    return output
