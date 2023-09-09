import vampytest

from ....user import User

from ...emoji import Emoji

from ..reaction_mapping import ReactionMapping


def test__ReactionMapping__new__no_parametres():
    """
    tests whether ``ReactionMapping.__new__`` works as intended.
    
    Case: No parameters.
    """
    reaction_mapping = ReactionMapping()
    
    vampytest.assert_instance(reaction_mapping, ReactionMapping)
    vampytest.assert_eq(len(reaction_mapping), 0)
    vampytest.assert_eq(reaction_mapping.fully_loaded, True)


def test__ReactionMapping__new__from_none():
    """
    tests whether ``ReactionMapping.__new__`` works as intended.
    
    Case: None.
    """
    reaction_mapping = ReactionMapping(None)
    
    vampytest.assert_instance(reaction_mapping, ReactionMapping)
    vampytest.assert_eq(len(reaction_mapping), 0)
    vampytest.assert_eq(reaction_mapping.fully_loaded, True)


def test__ReactionMapping__new__from_dictionary():
    """
    tests whether ``ReactionMapping.__new__`` works as intended.
    
    Case: dictionary.
    """
    emoji_1 = Emoji.precreate(202210010028)
    user_1 = User.precreate(202210010029)
    users = [user_1]
    
    reaction_mapping = ReactionMapping({emoji_1: users})
    
    vampytest.assert_instance(reaction_mapping, ReactionMapping)
    vampytest.assert_eq(len(reaction_mapping), len(users))
    vampytest.assert_eq(reaction_mapping.fully_loaded, True)
    
    vampytest.assert_in(emoji_1, reaction_mapping)
    vampytest.assert_eq(reaction_mapping[emoji_1], users)


def test__ReactionMapping__new__from_dictionary_with_unknown():
    """
    tests whether ``ReactionMapping.__new__`` works as intended.
    
    Case: contains unknown.
    """
    emoji_1 = Emoji.precreate(202210010030)
    user_1 = User.precreate(202210010031)
    users = [user_1, None]
    
    reaction_mapping = ReactionMapping({emoji_1: users})
    
    vampytest.assert_instance(reaction_mapping, ReactionMapping)
    vampytest.assert_eq(reaction_mapping.total_count, len(users))
    vampytest.assert_eq(reaction_mapping.fully_loaded, False)
    
    vampytest.assert_in(emoji_1, reaction_mapping)
    vampytest.assert_eq(reaction_mapping[emoji_1], [user_1, None])


def test__ReactionMapping__new__from_iterable():
    """
    tests whether ``ReactionMapping.__new__`` works as intended.
    
    Case: Iterable.
    """
    emoji_1 = Emoji.precreate(202210010032)
    user_1 = User.precreate(202210010033)
    users = [user_1, None]
    
    reaction_mapping = ReactionMapping([(emoji_1, users)])
    
    vampytest.assert_instance(reaction_mapping, ReactionMapping)
    vampytest.assert_eq(reaction_mapping.total_count, len(users))
    vampytest.assert_eq(reaction_mapping.fully_loaded, False)
    
    vampytest.assert_in(emoji_1, reaction_mapping)
    vampytest.assert_eq(reaction_mapping[emoji_1], users)


def test__ReactionMapping__new__type_error():
    """
    tests whether ``ReactionMapping.__new__`` works as intended.
    
    Case: `TypeError`.
    """
    emoji_1 = Emoji.precreate(202210010034)
    
    for input_value in (12.6, [12.6], [(12.6, [])], [(emoji_1, 12.6)]):
        with vampytest.assert_raises(TypeError):
            ReactionMapping(input_value)


def test__ReactionMapping__new__dictionary_with_empty_line():
    """
    tests whether ``ReactionMapping.__new__`` works as intended.
    
    Case: dictionary with empty value.
    """
    emoji_1 = Emoji.precreate(202210010038)
    users = []
    
    reaction_mapping = ReactionMapping({emoji_1: users})
    
    vampytest.assert_instance(reaction_mapping, ReactionMapping)
    vampytest.assert_eq(reaction_mapping.total_count, 0)
    vampytest.assert_eq(reaction_mapping.emoji_count, 0)
    vampytest.assert_eq(reaction_mapping.fully_loaded, True)
    
    vampytest.assert_not_in(emoji_1, reaction_mapping)
