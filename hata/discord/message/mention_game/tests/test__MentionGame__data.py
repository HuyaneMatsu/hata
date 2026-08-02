import vampytest

from ....bases import Icon, IconType
from ....core import MENTION_GAMES

from ..mention_game import MentionGame

from .test__MentionGame__constructor import _assert_fields_set


def test__MentionGame__from_data():
    """
    Tests whether ``MentionGame.from_data`` works as intended.
    """
    application_id = 202607040001
    icon = Icon(IconType.static, 2)
    name = 'Sanae'
    
    data = {
        'id': str(application_id),
        'icon_hash': icon.as_base_16_hash,
        'name': name,
    }
    
    mention_game = MentionGame.from_data(data)
    _assert_fields_set(mention_game)
    
    vampytest.assert_is(MENTION_GAMES.get(application_id, None), mention_game)
    
    vampytest.assert_eq(mention_game.icon, icon)
    vampytest.assert_eq(mention_game.id, application_id)
    vampytest.assert_eq(mention_game.name, name)


def test__MentionGame__to_data_data():
    """
    Tests whether ``MentionGame.to_data`` works as intended.
    """
    application_id = 202607040002
    icon = Icon(IconType.static, 2)
    name = 'Sanae'
    
    mention_game = MentionGame.precreate(
        application_id,
        icon = icon,
        name = name,
    )
    
    vampytest.assert_eq(
        mention_game.to_data(),
        {
            'id': str(application_id),
            'icon_hash': icon.as_base_16_hash,
            'name': name,
        },
    )
