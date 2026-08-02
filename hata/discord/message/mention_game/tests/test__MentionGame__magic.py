import vampytest

from ....bases import Icon, IconType

from ..mention_game import MentionGame


def test__MentionGame__repr__partial():
    """
    Tests whether ``MentionGame.__repr__`` works as intended.
    
    Case: partial.
    """
    icon = Icon(IconType.static, 2)
    name = 'Sanae'
    
    mention_game = MentionGame(
        icon = icon,
        name = name,
    )
    
    output = repr(mention_game)
    vampytest.assert_instance(output, str)


def test__MentionGame__repr():
    """
    Tests whether ``MentionGame.__repr__`` works as intended.
    """
    application_id = 202607040072
    icon = Icon(IconType.static, 2)
    name = 'Sanae'
    
    mention_game = MentionGame.precreate(
        application_id,
        icon = icon,
        name = name,
    )
    
    output = repr(mention_game)
    vampytest.assert_instance(output, str)


def test__MentionGame__hash__partial():
    """
    Tests whether ``MentionGame.__hash__`` works as intended.
    
    Case: partial.
    """
    icon = Icon(IconType.static, 2)
    name = 'Sanae'
    
    mention_game = MentionGame(
        icon = icon,
        name = name,
    )
    
    output = hash(mention_game)
    vampytest.assert_instance(output, int)


def test__MentionGame__hash():
    """
    Tests whether ``MentionGame.__hash__`` works as intended.
    """
    application_id = 202607040073
    icon = Icon(IconType.static, 2)
    name = 'Sanae'
    
    mention_game = MentionGame.precreate(
        application_id,
        icon = icon,
        name = name,
    )
    
    output = hash(mention_game)
    vampytest.assert_instance(output, int)


def _iter_options__eq__partial():
    icon = Icon(IconType.static, 2)
    name = 'Sanae'
    
    keyword_parameters = {
        'icon': icon,
        'name': name,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'icon': Icon(IconType.static, 5),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'Suwako',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__partial()).returning_last())
def test__MentionGame__eq__partial(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``MentionGame.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    mention_game_0 = MentionGame(**keyword_parameters_0)
    mention_game_1 = MentionGame(**keyword_parameters_1)
    
    output = mention_game_0 == mention_game_1
    vampytest.assert_instance(output, bool)
    return output


def test__MentionGame__eq():
    """
    Tests whether ``MentionGame.__eq__`` works as intended.
    """
    application_id = 202607040074
    icon = Icon(IconType.static, 2)
    name = 'Sanae'
    
    mention_game = MentionGame.precreate(
        application_id,
        icon = icon,
        name = name,
    )
    
    vampytest.assert_eq(mention_game, mention_game)
    vampytest.assert_eq(
        mention_game,
        MentionGame(
            icon = icon,
            name = name,
        ),
    )
    vampytest.assert_ne(
        mention_game,    
        MentionGame.precreate(
            202607040075,
            icon = icon,
            name = name,
        ),
    )
