import vampytest

from ....bases import Icon, IconType

from ..mention_game import MentionGame

from .test__MentionGame__constructor import _assert_fields_set


def test__MentionGame__copy():
    """
    Tests whether ``MentionGame.copy`` works as intended.
    """
    icon = Icon(IconType.static, 2)
    name = 'Sanae'
    
    mention_game = MentionGame(
        icon = icon,
        name = name,
    )
    
    copy = mention_game.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, mention_game)
    vampytest.assert_eq(copy, mention_game)


def test__MentionGame__copy_with__no_fields():
    """
    Tests whether ``MentionGame.copy_with`` works as intended.
    
    Case: no fields given.
    """
    icon = Icon(IconType.static, 2)
    name = 'Sanae'
    
    mention_game = MentionGame(
        icon = icon,
        name = name,
    )
    
    copy = mention_game.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, mention_game)
    vampytest.assert_eq(copy, mention_game)


def test__MentionGame__copy_with__all_fields():
    """
    Tests whether ``MentionGame.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_icon = Icon(IconType.static, 2)
    old_name = 'Sanae'
    
    new_icon = Icon(IconType.static, 5)
    new_name = 'Suwako'
    
    mention_game = MentionGame(
        icon = old_icon,
        name = old_name,
    )
    
    copy = mention_game.copy_with(
        icon = new_icon,
        name = new_name,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, mention_game)
    vampytest.assert_ne(copy, mention_game)
    
    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.name, new_name)



def _iter_options__icon_url():
    yield (
        202607040011,
        None,
        False,
    )
    
    yield (
        202607040012,
        Icon(IconType.animated, 5),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__icon_url()).returning_last())
def test__MentionGame__icon_url(application_id, icon):
    """
    Tests whether ``MentionGame.icon_url`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Identifier to create mention game with.
    
    icon : ``None | Icon``
        Icon to create the mention game with.
    
    Returns
    -------
    has_icon_url : `bool`
    """
    application = MentionGame.precreate(
        application_id,
        icon = icon,
    )
    
    output = application.icon_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__icon_url_as():
    yield (
        202607040013,
        None,
        {
            'ext': 'webp',
            'size': 128,
        },
        False,
    )
    
    yield (
        202607040014,
        Icon(IconType.animated, 5),
        {
            'ext': 'webp',
            'size': 128,
        },
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__icon_url_as()).returning_last())
def test__MentionGame__icon_url_as(application_id, icon, keyword_parameters):
    """
    Tests whether ``MentionGame.icon_url_as`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Identifier to create mention game with.
    
    icon : ``None | Icon``
        Icon to create the mention game with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_icon_url : `bool`
    """
    application = MentionGame.precreate(
        application_id,
        icon = icon,
    )
    
    output = application.icon_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def test__MentionGame__partial__true():
    """
    Tests whether ``MentionGame.partial`` works as intended.
    
    Case: true.
    """
    mention_game = MentionGame()
    output = mention_game.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__MentionGame__partial__false():
    """
    Tests whether ``MentionGame.partial`` works as intended.
    
    Case: false.
    """
    application_id = 202607040076
    
    mention_game = MentionGame.precreate(
        application_id = application_id,
    )
    output = mention_game.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
