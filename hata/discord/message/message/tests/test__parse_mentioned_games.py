import vampytest

from ...mention_game import MentionGame

from ..fields import parse_mentioned_games


def _iter_options():
    mention_game_0 = MentionGame.precreate(
        202607040015,
        name = 'Sane',
    )
    
    mention_game_1 = MentionGame.precreate(
        202607040016,
        name = 'Suwako',
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'mention_games': None,
        },
        None,
    )
    
    yield (
        {
            'mention_games': [],
        },
        None,
    )
    
    yield (
        {
            'mention_games': [
                mention_game_0.to_data(),
            ],
        },
        (mention_game_0,),
    )
    
    yield (
        {
            'mention_games': [
                mention_game_0.to_data(),
                mention_game_1.to_data(),
            ],
        },
        (
            mention_game_0,
            mention_game_1,
        ),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_mentioned_games(input_data):
    """
    Tests whether ``parse_mentioned_games`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | tuple<MentionGame>``
    """
    output = parse_mentioned_games(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, MentionGame)
    return output
