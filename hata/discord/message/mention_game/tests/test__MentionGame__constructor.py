import vampytest

from ....bases import Icon, IconType
from ....core import MENTION_GAMES

from ..mention_game import MentionGame


def _assert_fields_set(mention_game):
    """
    Asserts whether every fields are set of the given mention game.
    
    Parameters
    ----------
    mention_game : ``MentionGame``
        The instance to test.
    """
    vampytest.assert_instance(mention_game, MentionGame)
    vampytest.assert_instance(mention_game.icon, Icon)
    vampytest.assert_instance(mention_game.id, int)
    vampytest.assert_instance(mention_game.name, str)


def test__MentionGame__new__no_fields():
    """
    Tests whether ``MentionGame.__new__`` works as intended.
    
    Case: no fields given.
    """
    mention_game = MentionGame()
    _assert_fields_set(mention_game)


def test__MentionGame__new__all_fields():
    """
    Tests whether ``MentionGame.__new__`` works as intended.
    
    Case: all fields given.
    """
    icon = Icon(IconType.static, 2)
    name = 'Sanae'
    
    mention_game = MentionGame(
        icon = icon,
        name = name,
    )
    _assert_fields_set(mention_game)
    
    vampytest.assert_eq(mention_game.icon, icon)
    vampytest.assert_eq(mention_game.name, name)


def test__MentionGame__precreate__no_fields():
    """
    Tests whether ``MentionGame.precreate`` works as intended.
    
    Case: No fields given.
    """
    application_id = 202607040070
    
    mention_game = MentionGame.precreate(
        application_id,
    )
    _assert_fields_set(mention_game)
    
    vampytest.assert_eq(mention_game.id, application_id)
    
    vampytest.assert_is(MENTION_GAMES.get(application_id, None), mention_game)


def test__MentionGame__precreate__all_fields():
    """
    Tests whether ``MentionGame.precreate`` works as intended.
    
    Case: ALl fields given.
    """
    application_id = 202607040071
    icon = Icon(IconType.static, 2)
    name = 'Sanae'
    
    mention_game = MentionGame.precreate(
        application_id,
        icon = icon,
        name = name,
    )
    _assert_fields_set(mention_game)
    
    vampytest.assert_eq(mention_game.id, application_id)
    vampytest.assert_eq(mention_game.icon, icon)
    vampytest.assert_eq(mention_game.name, name)
    
    vampytest.assert_is(MENTION_GAMES.get(application_id, None), mention_game)
