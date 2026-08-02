import vampytest

from ...mention_game import MentionGame

from ..fields import put_mentioned_games


def _iter_options():
    mention_game_0 = MentionGame.precreate(
         202607040017,
        name = 'Sanae',
    )
    
    mention_game_1 = MentionGame.precreate(
        202607040018,
        name = 'Suwako',
    )
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'mention_games': [],
        },
    )
    
    yield (
        (
            mention_game_0,
            mention_game_1,
        ),
        False,
        {
            'mention_games': [
                mention_game_0.to_data(defaults = False),
                mention_game_1.to_data(defaults = False),
            ],
        },
    )
    
    yield (
        (
            mention_game_0,
            mention_game_1,
        ),
        True,
        {
            'mention_games': [
                mention_game_0.to_data(defaults = True),
                mention_game_1.to_data(defaults = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_mentioned_games(input_value, defaults):
    """
    Tests whether ``put_mentioned_games`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<MentionGame>``
        Value to serialize.
    
    defaults : `bool`
        Whether values as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_mentioned_games(input_value, {}, defaults)
